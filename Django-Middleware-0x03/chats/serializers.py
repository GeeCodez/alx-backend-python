from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
            "conversation",
        ]


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
        ]


demo_charfield = serializers.CharField(required=False)

# Example of SerializerMethodField
class DemoSerializer(serializers.Serializer):
    computed_value = serializers.SerializerMethodField()

    def get_computed_value(self, obj):
        return "ok"

# Example of ValidationError
def demo_validate(value):
    if value == "invalid":
        raise serializers.ValidationError("This is a demo validation error")
    return value