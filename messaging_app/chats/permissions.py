from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow access only to authenticated users who are participants
    of the conversation or message.
    """

    def has_permission(self, request, view):
        # Must be authenticated globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If the object *is* a Conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # If the object *is* a Message
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
