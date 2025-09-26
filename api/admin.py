# userprofile/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "avatar_img",
        "full_name",
        "employee_id",
        "email",
        "department",
        "designation",
        "employee_status",
        "phone",
        "join_date",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "employee_id",
        "department",
        "designation",
        "phone",
    )
    list_filter = (
        "department",
        "designation",
        "employee_status",
    )
    readonly_fields = ("avatar",)

    # Display user's full name
    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = "Name"
    full_name.admin_order_field = "user__first_name"

    # Display user's email
    def email(self, obj):
        return obj.user.email
    email.short_description = "Email"
    email.admin_order_field = "user__email"

    # Display avatar as image
    def avatar_img(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;" />', obj.avatar)
        return "-"
    avatar_img.short_description = "Avatar"
