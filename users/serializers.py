from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import Payment, CustomUser


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


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'avatar', 'phone_number', 'city', 'password', 'confirm_password',)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Пароли должны совпадать!")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и обновления пользователя"""
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'avatar', 'phone_number', 'city')
        read_only_fields = ('id',)


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'avatar', 'phone_number', 'city', 'is_active', 'is_staff', 'date_joined')
