from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at', 'short_content')
    list_filter = ('role', 'user')
    search_fields = ('user__username', 'content')
    ordering = ('-created_at',)

    def short_content(self, obj):
        return obj.content[:80]
    short_content.short_description = 'Content'
