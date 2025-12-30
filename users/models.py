from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class CustomUser(AbstractUser):
    """Модель пользователей"""

    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email']


class Payments(models.Model):
    """Модель платежей"""

    STATUS_CHOICES = [
        ('cash', 'наличные'),
        ('remittance', 'перевод'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateField(auto_now_add=True, verbose_name='дата платежа')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, verbose_name='оплаченный урок')
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(choices=STATUS_CHOICES, verbose_name='способ оплаты')
