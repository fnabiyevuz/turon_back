from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserDevice, UserActivity


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "middle_name", "email", "phone1", "phone2", "gender")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Extra", {"fields": ("uuid", "role")}),
    )
    readonly_fields = ("uuid",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "first_name", "last_name", "middle_name", "email", "phone1", "phone2", "gender", "role"),
            },
        ),
    )
    list_display = ("username", "first_name", "last_name", "role", "gender", "phone1", "is_staff")
    search_fields = ("username", "first_name", "last_name", "phone1", "phone2")
    ordering = ("last_name", "first_name")


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "device_name", "ip_address", "last_activity")
    search_fields = ("user__username", "device_name", "ip_address")
    list_filter = ("last_activity",)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "active_time")
    list_filter = ("date", "user")
    search_fields = ("user__username", "user__first_name", "user__last_name")