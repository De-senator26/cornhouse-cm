"""Admin registration for custom User model."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """Custom admin for User with CornHouse fields."""
    model = User
    list_display = ('username', 'email', 'phone', 'role', 'is_staff', 'is_verified')
    list_filter = ('role', 'is_verified', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('CornHouse Info', {'fields': ('phone', 'role', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('CornHouse Info', {'fields': ('phone', 'role')}),
    )
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
