from django.contrib import admin

from groups.models import GroupChat


@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ['name','avatar' ,'leader']
    search_fields = ['name', 'leader']
    ordering = ['name']
