from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Payment
from users.serializers import PaymentSerializer, MyTokenObtainPairSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet для оплат"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter,]
    ordering_fields = ['date', 'course', 'lesson', 'payment_method']


class MyTokenObtainPairView(TokenObtainPairView):
    """Представление для получения JWT токена"""
    serializer_class = MyTokenObtainPairSerializer
