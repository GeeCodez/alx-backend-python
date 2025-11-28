from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render
from django.contrib import messages
from django.db.models import Prefetch, Q
from .models import Message

User=get_user_model

@login_required
def delete_user(request):
    user=request.user
    if request.method=='POST':
        user.delete()
        messages.success(request,'Your account has been deleted succesfully')
        return redirect('home')
    return render(request,'messaging/confirm_delete.html')


@login_required
def conversation_list(request):

    messages_qs = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        parent_message=None
    ).select_related(
        "sender",
        "receiver",
        "parent_message"
    ).prefetch_related(
        Prefetch(
            "replies",
            queryset=Message.objects.select_related("sender", "receiver", "parent_message")
        )
    )

    conversations = [msg.get_thread() for msg in messages_qs]

    return render(request, "messaging/conversation_list.html", {
        "conversations": conversations
    })