from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'email', 'phone', 'city', 'is_staff', 'is_active')  # убрали username
    search_fields = ('email', 'phone', 'city')  # убрали username
    list_filter = ('is_staff', 'is_active', 'city')
    ordering = ('email',)  # добавили ordering, чтобы не было ошибок

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'city', 'avatar')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'city', 'avatar')}),
    )
