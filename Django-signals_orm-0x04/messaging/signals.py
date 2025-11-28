from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model

@receiver(post_save,sender=Message)
def create_notification_for_message(sender,instance,created,**kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save,sender=Message)
def log_message_edit(sender,instance,**kwargs):
    if instance.pk:
        old_message=Message.objects.get(pk=instance.pk)
        if old_message.content!=instance.content:
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content
            )
            instance.edited=True

User=get_user_model

@receiver(post_delete,sender=User)
def delete_user_related_data(sender,instance,**kwargs):
    """
    Deletes all data related to a deleted user's account
    """

    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    Notification.objects.filter(User=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()