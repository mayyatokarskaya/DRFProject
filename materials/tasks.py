from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from materials.models import Course

from django.utils import timezone
from datetime import timedelta

from .models import Course, Lesson, Subscription


@shared_task
# def send_course_update_email(user_email, course_title):
#     subject = f"Обновление курса: {course_title}"
#     message = f"Курс '{course_title}' был обновлён. Проверьте новые материалы!"
#     from_email = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [user_email]
#
#     send_mail(subject, message, from_email, recipient_list)
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    # Проверка, что курс не обновлялся последние 4 часа
    if course.updated_at < timezone.now() - timedelta(hours=4):
        subscribers = Subscription.objects.filter(course=course).values_list('user__email', flat=True)
        for email in subscribers:
            subject = f"Обновление курса: {course.title}"
            message = f"Курс '{course.title}' был обновлён. Проверьте новые материалы!"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
