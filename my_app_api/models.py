from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
import uuid

class Visiteur(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.uuid)

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    visiteur = models.ForeignKey(Visiteur, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f'Conversation {self.id} with registered user {self.user}'
        elif self.visiteur:
            return f'Conversation {self.id} with visitor {self.visiteur}'
        else:
            return f'Conversation {self.id} without participant'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=False) | models.Q(visiteur__isnull=False),
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

class Produit(models.Model):
    produit_id = models.CharField(max_length=255, primary_key=True)
    nom = models.CharField(max_length=255)
#     description = models.TextField(null=True, blank=True)
#     prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom

class Favori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'produit'),)  # Cette contrainte assure qu'un utilisateur ne peut pas marquer le même produit comme favori plusieurs fois

    def __str__(self):
        return f'Favori {self.id} - {self.produit.nom} par {self.user.username}'