# messages/models.py
from django.db import models
from django.conf import settings
from .managers import UnreadMessagesManager
class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    edited=models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read=models.BooleanField(default=False)
    objects = models.Manager()              # default manager
    unread = UnreadMessagesManager()        # custom manager

    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='edited_messages'
    )
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    def get_thread(self):
        thread = {
            "message": self,
            "replies": []
        }

        replies = self.replies.all().select_related("sender", "receiver")

        for reply in replies:
            thread["replies"].append(reply.get_thread())

        return thread



    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(
        'Message',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']  # newest notifications first
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"Notification for {self.user} about Message {self.message.id}"

# messages/models.py
class MessageHistory(models.Model):
    message = models.ForeignKey(
        'Message',
        on_delete=models.CASCADE,
        related_name='history'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"
