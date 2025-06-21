from django.db import models
from materials.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="stripe_payments"  # 👈 Уникальное имя для связи
    )
    stripe_session_id = models.CharField(max_length=255)
    stripe_payment_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.course} - {self.created_at}"
