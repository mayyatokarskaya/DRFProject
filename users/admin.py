from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Payment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("id", "email", "phone", "city", "is_staff", "is_active")  # убрали username
    search_fields = ("email", "phone", "city")  # убрали username
    list_filter = ("is_staff", "is_active", "city")
    ordering = ("email",)  # добавили ordering, чтобы не было ошибок

    fieldsets = BaseUserAdmin.fieldsets + ((None, {"fields": ("phone", "city", "avatar")}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + ((None, {"fields": ("phone", "city", "avatar")}),)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "payment_date", "paid_course", "paid_lesson", "amount", "payment_method")
    list_filter = ("payment_method",)
    search_fields = ("user__username", "paid_course__title", "paid_lesson__title")
