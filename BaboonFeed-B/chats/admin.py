from django.contrib import admin

from .models import Message, Chat

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'created_at', 'author', 'receiver', 'chat', 'group')
    search_fields = ('content', 'author__username', 'receiver__username')
    list_filter = ('created_at', 'author', 'receiver', 'chat', 'group')
    ordering = ('-created_at',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_modified', 'last_message')
    list_filter = ('last_modified',)
    ordering = ('-last_modified',)