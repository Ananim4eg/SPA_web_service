from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Представление ViewSet для работы с курсами"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsModerator]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'detail':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'delete':
            self.permission_classes = [IsAuthenticated, ~IsModerator & IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateApiView(generics.CreateAPIView):
    """Представление для создания уроков"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(generics.ListAPIView):
    """Представление для просмотра списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]
    pagination_class = CustomPagination


class LessonRetrieveApiView(generics.RetrieveAPIView):
    """Представление для просмотра отдельных уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateApiView(generics.UpdateAPIView):
    """Представление для обновления уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDeleteApiView(generics.DestroyAPIView):
    """Представление для удаления уроков"""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner & ~IsModerator]


class SubscribeToCourseView(APIView):
    """Представление для подписки/отписки на курсы"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        course = Course.objects.get(id=course_id)

        try:
            # Ищем существующую подписку
            subscription = Subscription.objects.get(
                user=request.user,
                course=course
            )

            # Переключаем статус подписки
            subscription.is_active = not subscription.is_active
            subscription.save()

            # Формируем ответное сообщение
            action = 'отписан от курса' if not subscription.is_active else 'подписан на курс'
            message = f'Успешно {action} {course.course_name}'

            return Response({
                'message': message,
            }, status=status.HTTP_200_OK)

        except:
            # Подписка не найдена - создаем ее.
            Subscription.objects.create(
                user=request.user,
                course=course
            )

            return Response({
                'message': f'Успешно подписан на курс {course.course_name}'
            }, status=status.HTTP_201_CREATED)
