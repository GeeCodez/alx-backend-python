from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render
from django.contrib import messages
from django.views.decorators.cache import cache_page
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
@cache_page(60)
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

@login_required
def unread_inbox(request):
    """
    Use the custom manager to get unread messages for the logged-in user.
    Optimize by selecting only necessary fields with .only()
    """
    unread_qs = Message.unread.unread_for_user(request.user).only(
        "id", "content", "sender", "timestamp", "parent_message"
    ).select_related("sender", "parent_message")

    # Optional: prefetch replies for these unread messages if needed
    unread_qs = unread_qs.prefetch_related(
        Prefetch(
            "replies",
            queryset=Message.objects.select_related("sender").only("id", "content", "sender", "timestamp", "parent_message")
        )
    )

    return render(request, "messaging/unread_inbox.html", {
        "messages": unread_qs
    })

