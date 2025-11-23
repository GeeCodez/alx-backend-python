from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only allow participants of a conversation to interact with it or its messages.
    """

    def has_permission(self, request, view):
        # Must be authenticated globally
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow authenticated users to create conversations
        if view.basename == "conversation" and request.method == "POST":
            return True

        return True  # Other checks handled in object permission

    def has_object_permission(self, request, view, obj):

        # Allow safe methods (GET, HEAD, OPTIONS) but ONLY if user is a participant
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, "participants"):
                return request.user in obj.participants.all()
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.participants.all()
            return False

        # For modifying (POST, PUT, PATCH, DELETE) → must be participant
        if request.method in ["PUT", "PATCH", "DELETE", "POST"]:
            if hasattr(obj, "participants"):
                return request.user in obj.participants.all()
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.participants.all()
            return False

        return False
