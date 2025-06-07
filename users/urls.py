from django.urls import path
from .views import PaymentViewSet, UserProfileView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
] + router.urls