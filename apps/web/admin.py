"""Admin configuration for web app models."""
from django.contrib import admin
from .models import UserFeedback


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    """Admin configuration for UserFeedback."""
    list_display = ('get_author', 'rating', 'category', 'role', 'is_public', 'created_at')
    list_filter = ('rating', 'category', 'role', 'is_public', 'created_at')
    search_fields = ('name', 'comment', 'user__username', 'user__email')
    list_editable = ('is_public',)

    @admin.display(description='User / Name')
    def get_author(self, obj):
        if obj.user:
            return f"{obj.user.username} ({obj.user.email or 'No email'})"
        return obj.name or "Anonymous"
