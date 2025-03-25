from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'avatar', 'bio']
