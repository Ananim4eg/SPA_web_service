from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для оплат"""
    class Meta:
        model = Payment
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для токенов"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token
