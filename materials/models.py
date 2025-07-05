from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    preview = models.ImageField(upload_to="courses/", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", related_name="courses"
    )


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE, verbose_name="Курс")
    title = models.CharField(max_length=255, verbose_name="Название")
    preview = models.ImageField(upload_to="lessons/", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")
    video_url = models.URLField(verbose_name="Ссылка на видео")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", related_name="lessons"
    )


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="subscriptions")

    class Meta:
        unique_together = ("user", "course")  # Один пользователь — одна подписка на курс

    def __str__(self):
        return f"{self.user} подписан на {self.course}"
