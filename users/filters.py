from django_filters import rest_framework as filters
from .models import Payment


class PaymentFilter(filters.FilterSet):
    paid_course = filters.NumberFilter(field_name="paid_course__id")
    paid_lesson = filters.NumberFilter(field_name="paid_lesson__id")
    payment_method = filters.CharFilter(field_name="payment_method")
    ordering = filters.OrderingFilter(
        fields=(("payment_date", "date"),),
        field_labels={
            "payment_date": "Дата оплаты",
        },
    )

    class Meta:
        model = Payment
        fields = ["paid_course", "paid_lesson", "payment_method"]
