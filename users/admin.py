from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Payment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("id", "email", "phone", "city", "is_staff", "is_active")
    search_fields = ("email", "phone", "city")
    list_filter = ("is_staff", "is_active", "city")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone", "city", "avatar")}),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
        (
            "Additional info",
            {
                "fields": ("first_name", "last_name", "phone", "city", "avatar"),
            },
        ),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "payment_date", "paid_course", "paid_lesson", "amount", "payment_method")
    list_filter = ("payment_method",)
    search_fields = (
        "user__email",
        "paid_course__title",
        "paid_lesson__title",
    )  # Изменили user__username на user__email
