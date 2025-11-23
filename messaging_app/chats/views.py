from rest_framework import viewsets, filters,status,
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])
        if not participants or len(participants) < 1:
            return Response(
                {"detail": "A conversation must have at least 2 participants."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Automatically add creator
        if request.user.user_id not in participants:
            participants.append(request.user.user_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()

        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering = ['timestamp']

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        if not conversation_id:
            return Response(
                {"detail": "Conversation ID is required."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation does not exist.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(conversation=conversation, sender=request.user)

        return Response(serializer.data)
