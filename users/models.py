from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Модель пользователей"""

    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email']


class Payment(models.Model):
    """Модель платежей"""

    STATUS_CHOICES = [
        ('cash', 'наличные'),
        ('remittance', 'перевод'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateField(auto_now_add=True, verbose_name='дата платежа')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='оплаченный курс', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, verbose_name='оплаченный урок', null=True, blank=True)
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(choices=STATUS_CHOICES, verbose_name='способ оплаты')
