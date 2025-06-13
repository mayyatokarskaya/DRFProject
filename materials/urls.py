from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonRetrieveUpdateAPIView,
    LessonListAPIView,
    LessonDestroyAPIView,
    SubscriptionToggleAPIView,
)

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/<int:pk>/", LessonRetrieveUpdateAPIView.as_view(), name="lesson-detail"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson-delete"),
    path("lessons/create/", LessonCreateAPIView.as_view()),
    path("subscribe/", SubscriptionToggleAPIView.as_view(), name="toggle-subscription"),
] + router.urls
