from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Return a queryset of unread messages for the given user.
        Do not call .only() here so caller can chain .only() as required.
        """
        return self.get_queryset().filter(
            receiver=user,
            read=False
        )
