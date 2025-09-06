import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from django.utils import timezone
from datetime import timedelta

from .models import Course,Subscription

logger = logging.getLogger(__name__)


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    # Проверка, что курс не обновлялся последние 4 часа
    if course.updated_at < timezone.now() - timedelta(hours=4):
        subscribers = Subscription.objects.filter(course=course).values_list('user__email', flat=True)
        for email in subscribers:
            subject = f"Обновление курса: {course.title}"
            message = f"Курс '{course.title}' был обновлён. Проверьте новые материалы!"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


@shared_task
def check_inactive_users():
    """Блокировка пользователей, не заходивших больше месяца."""
    User = get_user_model()
    one_month_ago = timezone.now() - timedelta(days=30)  # Можно изменить на 31 день

    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,  # last_login старше месяца
        is_active=True  # Блокируем только активных
    )

    count = inactive_users.update(is_active=False)  # Массовое обновление

    logger.info(f"Заблокировано {count} неактивных пользователей.")
    return f"Заблокировано {count} пользователей."