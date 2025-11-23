from django.contrib import admin
from .models import User

@admin.register(User)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "username")
    search_fields = ("first_name", "user_id")
    list_filter = ("role",)
