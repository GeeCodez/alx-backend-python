import uuid 
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Replace Django's default integer ID with UUID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #first_name, lastname, username, and password are already in the Abstract user class
    phone_number=models.CharField(max_length=20,null=True,blank=True)
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    # Use email as the unique login identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Django needs at least one non-email field

    # Make email unique
    email = models.EmailField(unique=True)


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # A conversation has multiple participants (many-to-many users)
    participants = models.ManyToManyField(User, related_name='conversations')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["sent_at"]),
        ]

    def __str__(self):
        return f"Message {self.id} from {self.sender.email}"
