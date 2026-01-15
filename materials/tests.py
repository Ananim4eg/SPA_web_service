from lib2to3.pgen2.tokenize import group

from django.contrib.auth.models import Group
from django.template.context_processors import request
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase

from materials.models import Lesson, Course
from users.models import CustomUser


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email="admin1@example.com")
        self.course = Course.objects.create(course_name="Начальный уровень", owner=self.user)
        self.lesson = Lesson.objects.create(lesson_name="Геометрия", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson_get', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('lesson_name'), self.lesson.lesson_name
        )

    def test_lesson_create(self):
        url = reverse('materials:lesson_create')
        data = {
            'lesson_name': 'Физика',
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse('materials:lesson_update', args=(self.lesson.pk,))
        data = {
            'lesson_name': 'Химия'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('lesson_name'), 'Химия'
        )

    def test_lesson_delete(self):
        url = reverse('materials:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        self.group, created = Group.objects.get_or_create(name='moderator')
        self.user.groups.add(self.group)
        self.user.save()
        url = reverse('materials:lesson_list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.pk,
                    'video_url': None,
                    'lesson_name': self.lesson.lesson_name,
                    'description': None,
                    'preview_lesson': None,
                    'course': self.course.pk,
                    'owner': self.user.pk}
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class CourseSubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="admin1@example.com")
        self.course = Course.objects.create(course_name="Начальный уровень")
        self.client.force_authenticate(user=self.user)

    def test_course_subscription(self):
        url = reverse('materials:subscribe_course')
        data = {
            "course_id": self.course.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        url1 = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.get(url1)

        self.assertEqual(
            response.json()['is_subscribed'], True
        )

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        url1 = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.get(url1)

        self.assertEqual(
            response.json()['is_subscribed'], False
        )
