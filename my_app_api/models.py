from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Les utilisateurs doivent avoir une adresse e-mail')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
class Visitor(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    browser = models.CharField(max_length=255, null=True, blank=True)
    os = models.CharField(max_length=255, null=True, blank=True)
    device = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return str(self.uuid)

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f'Conversation {self.id} with registered user {self.user}'
        elif self.visitor:
            return f'Conversation {self.id} with visitor {self.visitor}'
        else:
            return f'Conversation {self.id} without participant'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=False) | models.Q(visitor__isnull=False),
                name='conversation_has_either_user_or_visitor'
            )
        ]

class Message(models.Model):
    TYPE_CHOICES = [
        ('Human', 'Human'),
        ('AI', 'AI'),
    ]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=11, choices=TYPE_CHOICES)

    def __str__(self):
        return f'Message {self.id} in conversation {self.conversation.id}'

class Gender(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return f'Favori {self.id} - {self.product.name} par {self.user.username}'

class AgeRange(models.Model):
    age_range = models.CharField(max_length=255)

    def __str__(self):
        return self.age_range

class Occasion(models.Model):
    occasion_name = models.CharField(max_length=255)

    def __str__(self):
        return self.occasion_name

class Relationship(models.Model):
    relationship_type = models.CharField(max_length=255)

    def __str__(self):
        return self.relationship_type

class ActivityInterest(models.Model):
    activity = models.CharField(max_length=255)

    def __str__(self):
        return self.activity

class PersonalityPreference(models.Model):
    personality = models.CharField(max_length=255)

    def __str__(self):
        return self.personality

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    typology = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(max_length=2048, null=True, blank=True)
    target_budget = models.CharField(max_length=255, null=True, blank=True)
    fixed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=2048, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    age_ranges = models.ManyToManyField(AgeRange, blank=True)
    occasions = models.ManyToManyField(Occasion, blank=True)
    relationships = models.ManyToManyField(Relationship, blank=True)
    activities_interests = models.ManyToManyField(ActivityInterest, blank=True)
    personalities_preferences = models.ManyToManyField(PersonalityPreference, blank=True)

    def __str__(self):
        return self.name

class Favori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'product'),)  # Cette contrainte assure qu'un utilisateur ne peut pas marquer le même produit comme favori plusieurs fois

class Article(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)