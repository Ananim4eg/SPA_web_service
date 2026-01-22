from celery import shared_task
from config import settings
from django.core.mail import send_mail


@shared_task
def send_message_about_update(emails, course_name):
    send_mail(
        "Обновление курса",
        f'Курс "{course_name}" - обновился!',
        settings.EMAIL_HOST_USER,
        [*emails]
    )