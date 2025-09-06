from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsModerator
from .models import Course, Lesson, Subscription
from .permissions import IsOwnerOrModerator
from .serializers import CourseSerializer, LessonSerializer
from .paginators import StandardResultsSetPagination

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .tasks import send_course_update_email


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


    @swagger_auto_schema(operation_description="Получить список всех курсов")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Создать новый курс (только для аутентифицированных пользователей)")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Получить курс по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Обновить курс (владелец или модератор)")
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            course = self.get_object()  # обновлённый объект курса
            # Получаем список email подписчиков
            # subscribers = Subscription.objects.filter(course=course).values_list('user__email', flat=True)
            # Запускаем асинхронную задачу для каждого подписчика
            # for email in subscribers:
            #     send_course_update_email.delay(email, course.title)
            send_course_update_email.delay(course.id)  # Передаём ID курса вместо email

        return response

    @swagger_auto_schema(operation_description="Удалить курс (владелец)")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_description="Создать новый урок (только для администратора)")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    @swagger_auto_schema(operation_description="Получить урок по ID")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Обновить урок (владелец или модератор)")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Удалить урок (владелец или модератор)")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(operation_description="Получить список уроков (модератор или админ)")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubscriptionToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Добавить или удалить подписку на курс. Если подписка уже существует — она будет удалена.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["course_id"],
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID курса для подписки'),
            },
        ),
        responses={
            200: openapi.Response(description="Успешное добавление или удаление подписки"),
            404: openapi.Response(description="Курс не найден")
        }
    )
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
