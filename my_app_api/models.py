from django.db import models
from django.contrib.auth.models import User
import uuid

class User(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # Consider using Django's built-in User model or a hashed password field

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation {self.id} with {self.user}'

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
