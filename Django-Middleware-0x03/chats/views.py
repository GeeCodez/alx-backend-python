from rest_framework.viewsets import ModelViewSet
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .pagination import MessagePagination

class ConversationViewset(ModelViewSet):
    serializer_class = ConversationSerializer
    
    def get_queryset(self):
        user=self.request.user
        return Conversation.objects.filter(participants=user)
    
    def perform_create(self, serializer):
        Conversation=serializer.save()
        Conversation.participants.add(self.request.user)



class MessageViewset(ModelViewSet):
    serializer_class = MessageSerializer
    pagination_class=MessagePagination

    def get_queryset(self):
        user=self.request.user
        return Message.objects.filter(Conversation__participants=user)

    def perform_create(self, serializer):
        conversation=serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise PermissionError('You are not a participant of the conversation')
        serializer.save(sender=self.request.user)