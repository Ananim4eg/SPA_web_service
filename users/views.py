from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Payment, CustomUser
from users.serializers import PaymentSerializer, MyTokenObtainPairSerializer, UserRegistrationSerializer, \
    UserSerializer, AdminUserListSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet для оплат"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter,]
    ordering_fields = ['date', 'course', 'lesson', 'payment_method']


class MyTokenObtainPairView(TokenObtainPairView):
    """Представление для получения JWT токена"""
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):
    """Представление для регистрации"""

    @swagger_auto_schema(
        operation_description="Регистрация",
        operation_summary="Регистрация нового пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description='Почта'),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
                "confirm_password": openapi.Schema(type=openapi.TYPE_STRING, description='Подтверждение пароля')
            },
            required=['email', "password", "confirm_password"]
        ),
        responses={
            201: openapi.Response(
                description="1"
            ),
            400: "Ошибка валидации данных"
        },
        tags=['register']
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    """Представление для просмотра списка пользователей"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(RetrieveAPIView):
    """Представление для просмотра отдельного пользователя"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserUpdateView(UpdateAPIView):
    """Представление для обновления пользователя"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDeleteView(DestroyAPIView):
    """Представление для удаления пользователя"""
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class AdminUserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AdminUserListSerializer
    permission_classes = [IsAdminUser]
