from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from users.permissions import IsModerator
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework import generics


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """Разделение прав по действиям"""
        if self.action in ['create', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['update', 'partial_update', 'retrieve', 'list']:
            return [IsAuthenticated(), IsModerator() | IsAdminUser()]
        return [IsAdminUser()]


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]  # Только админ

class LessonRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]  # Модератор или админ

class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]  # Только админ
