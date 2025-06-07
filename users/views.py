from rest_framework import viewsets, generics
from .models import Payment
from .serializers import PaymentSerializer, UserProfileSerializer
from .filters import PaymentFilter
from django_filters import rest_framework as django_filters


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = PaymentFilter

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user