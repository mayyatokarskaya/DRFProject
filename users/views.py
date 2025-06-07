from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter
from django_filters import rest_framework as django_filters


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = PaymentFilter