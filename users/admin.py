from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'phone', 'city', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'phone', 'city')
    list_filter = ('is_staff', 'is_active', 'city')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'city', 'avatar')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'city', 'avatar')}),
    )
