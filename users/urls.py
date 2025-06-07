from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    PaymentViewSet,
    UserProfileView,
    UserRegisterView,
    UserListView,
    UserDetailView,
    CustomTokenObtainPairView,
)

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    # Профиль пользователя (существующий эндпоинт)
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    # Новые эндпоинты для аутентификации и пользователей
    path("register/", UserRegisterView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("me/", UserDetailView.as_view(), name="user-detail"),
] + router.urls
