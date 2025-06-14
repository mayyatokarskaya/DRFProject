from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from materials.models import Course, Lesson, Subscription


class CourseLessonSubscriptionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаём пользователя и делаем его админом (is_staff=True)
        self.user = get_user_model().objects.create_user(
            email='user1@example.com', password='pass123'
        )
        self.user.is_staff = True
        self.user.save()

        # Другой пользователь (не админ)
        self.other_user = get_user_model().objects.create_user(
            email='user2@example.com', password='pass456'
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title='Курс A', description='Описание курса', owner=self.user)
        self.lesson = Lesson.objects.create(title='Урок 1', course=self.course, owner=self.user)

        self.lesson_url = reverse('lesson-detail', kwargs={'pk': self.lesson.pk})
        self.lesson_create_url = reverse('lesson-create')
        self.subscribe_url = reverse('toggle-subscription')

    def test_create_lesson(self):
        data = {
            'title': 'Новый урок',
            'description': 'Описание',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/watch?v=kTlv5_Bs8aw&list=RDkTlv5_Bs8aw&start_radio=1'
        }
        response = self.client.post(self.lesson_create_url, data)
        print(response.data)  # Добавь эту строку, чтобы увидеть ошибки валидации
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_lesson(self):
        response = self.client.get(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Урок 1')

    def test_update_lesson(self):
        data = {'title': 'Обновлённый урок'}
        response = self.client.patch(self.lesson_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Обновлённый урок')

    def test_delete_lesson(self):
        response = self.client.delete(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_user_cannot_update_or_delete(self):
        self.client.force_authenticate(user=self.other_user)

        # Попытка обновить урок другого пользователя
        data = {'title': 'Второй пользователь обновляет'}
        response = self.client.patch(self.lesson_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Попытка удалить урок другого пользователя
        response = self.client.delete(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access_denied(self):
        self.client.force_authenticate(user=None)

        # Попытка получить урок без авторизации
        response = self.client.get(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Попытка создать урок без авторизации
        data = {
            'title': 'Урок без авторизации',
            'description': 'Описание',
            'course': self.course.id
        }
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscription_add(self):
        response = self.client.post(self.subscribe_url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_remove(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(self.subscribe_url, {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_other_user_cannot_update(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(self.lesson_url, {'title': 'Хак'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)