from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import ConversationViewset , MessageViewset

NestedDefaultRouter = "NestedDefaultRouter"
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewset, basename='conversation')
router.register(r'messages', MessageViewset, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
