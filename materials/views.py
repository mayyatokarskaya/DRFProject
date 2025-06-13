from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsModerator
from .models import Course, Lesson, Subscription
from .permissions import IsOwner, IsOwnerOrModerator
from .serializers import CourseSerializer, LessonSerializer
from .paginators import StandardResultsSetPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "retrieve"]:
            return [IsAuthenticated(), IsOwnerOrModerator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]
    pagination_class = StandardResultsSetPagination


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class SubscriptionToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
