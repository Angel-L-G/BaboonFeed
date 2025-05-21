from django.contrib import admin

from posts.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'content', 'file', 'user']
    search_fields = ['user', 'pk']
    ordering = ['created_at']