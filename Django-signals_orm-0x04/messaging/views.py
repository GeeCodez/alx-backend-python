from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render
from django.contrib import messages

User=get_user_model

@login_required
def delete_user(request):
    user=request.user
    if request.method=='POST':
        user.delete()
        messages.success(request,'Your account has been deleted succesfully')
        return redirect('home')
    return render(request,'messaging/confirm_delete.html')