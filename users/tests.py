from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from materials.models import Lesson, Course
from users.models import CustomUser, Subscribe


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email='test@mail.ru')
        self.course = Course.objects.create(name='1 курс', owner=self.user)
        self.lesson = Lesson.objects.create(name='Математика', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)


    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )


    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "name": "Русский язык",
            "course": self.course.pk,
            "owner": self.user.pk
        }
        response = self.client.post(url,data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Русский язык",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Русский язык"
        )


    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )


    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        data = response.json()
        result = {
    "count": 1,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": self.lesson.pk,
            "video_url": None,
            "name": self.lesson.name,
            "description": None,
            "preview": None,
            "course": self.course.pk,
            "owner": self.user.pk
        }
    ]
}
        self.assertEqual(
            data, result
        )


    def test_lesson_retrieve_unauthenticated(self):
        self.client.force_authenticate(user=None)  # разлогиниваем
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_lesson_update_as_moderator(self):
        # Создаем пользователся модератора и добавляем его в группу "moders"
        moderator = CustomUser.objects.create(email='moderator@mail.ru')
        self.group_moders, _ = Group.objects.get_or_create(name="moders")
        # Получаем группу moders
        group_moders = Group.objects.get(name='moders')
        # Добавляем пользователя в группу
        moderator.groups.add(group_moders)
        # Аутентифицируемся как модератор
        self.client.force_authenticate(user=moderator)

        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"name": "Физика"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Физика")


class SubscribeTestCase(APITestCase):
    def setUp(self):
        # Настройка начальных данных
        self.user = CustomUser.objects.create(email='test@mail.ru')
        self.course = Course.objects.create(name='1 курс', owner=self.user)
        self.url = reverse('users:subscribe')
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        data = {
            "course": self.course.pk
        }
        response = self.client.post(self.url, data)

        # Проверяем успешность операции
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'подписано')

        # Проверяем, что подписка была создана
        subscription_exists = Subscribe.objects.filter(user=self.user, course=self.course).exists()
        self.assertTrue(subscription_exists)

    def test_unsubscribe_from_course(self):
        # Сначала создаем подписку
        Subscribe.objects.create(user=self.user, course=self.course)

        data = {
            "course": self.course.pk
        }
        response = self.client.post(self.url, data)

        # Проверяем успешность операции
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'отписано')

        # Проверяем, что подписка удалена
        subscription_exists = Subscribe.objects.filter(user=self.user, course=self.course).exists()
        self.assertFalse(subscription_exists)

    def test_subscribe_to_course_unauthenticated(self):
        self.client.force_authenticate(user=None)  # разлогиниваем
        data = {
            "course": self.course.pk
        }
        response = self.client.post(self.url, data)

        # Проверяем успешность операции
        self.assertEqual(response.status_code, 401)


        # Проверяем, что подписка не была создана
        subscription_exists = Subscribe.objects.filter(user=self.user, course=self.course).exists()
        self.assertFalse(subscription_exists)


    def test_subscribe_to_course_error_course(self):
        data = {
            "course": 1000
        }
        response = self.client.post(self.url, data)

        # Проверяем успешность операции
        self.assertEqual(response.status_code, 404)


        # Проверяем, что подписка не была создана
        subscription_exists = Subscribe.objects.filter(user=self.user, course=self.course).exists()
        self.assertFalse(subscription_exists)
