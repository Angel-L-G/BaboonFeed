from django.contrib import admin

from groups.models import GroupChat


@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name','avatar' ,'leader', 'last_message', 'last_modified']
    search_fields = ['name', 'leader']
    ordering = ['name']
