from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants")

        if not participants or len(participants) < 2:
            raise ValidationError("A conversation must have at least 2 participants.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")

        if not conversation_id:
            raise ValidationError("conversation ID is required.")

        if not sender_id:
            raise ValidationError("sender ID is required.")

        # Ensure conversation exists
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation does not exist.")

        # Validate and save message
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(conversation=conversation)

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
