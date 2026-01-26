from datetime import datetime, timedelta

from celery import shared_task
from django.utils import timezone

from config import settings
from django.core.mail import send_mail

from users.models import CustomUser


@shared_task
def send_message_about_update(emails, course_name):
    """Отправка уведомления об обновлении курса"""
    send_mail(
        "Обновление курса",
        f'Курс "{course_name}" - обновился!',
        settings.EMAIL_HOST_USER,
        [*emails]
    )


@shared_task
def disable_user():
    """Отключение пользователей, которые не были онлайн в течение месяца"""
    date_point = timezone.now() - timedelta(days=30)
    users_list = CustomUser.objects.filter(is_active=True, last_login__lt=date_point)

    for user in users_list:
        user.is_active=False
        user.save()
