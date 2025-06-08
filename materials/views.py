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
