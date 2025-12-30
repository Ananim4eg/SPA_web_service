from django.core.management.base import BaseCommand
from materials.models import Course, Lesson
from users.models import CustomUser, Payment


class Command(BaseCommand):
    help = 'Наполнение таблицы платежей данными'

    def handle(self, *args, **kwargs):

        CustomUser.objects.all().delete()
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Payment.objects.all().delete()

        user = CustomUser.objects.create_user(
            email='test_user@example.com',
            password='Test123!',
        )
        user.save()

        course = Course.objects.create(
            course_name='ознакомительный курс'
        )
        course.save()

        lesson = Lesson.objects.create(
            lesson_name='первое занятие',
            course=Course.objects.first()
        )
        lesson.save()

        lesson1 = Lesson.objects.create(
            lesson_name='второе занятие',
            course=Course.objects.first()
        )
        lesson1.save()

        payment_cash_course = Payment.objects.create(
            user=CustomUser.objects.get(email='test_user@example.com'),
            course=Course.objects.first(),
            amount=1430,
            payment_method='cash'
        )
        payment_cash_course.save()

        payment_cash_lesson = Payment.objects.create(
            user=CustomUser.objects.get(email='test_user@example.com'),
            lesson=Lesson.objects.first(),
            amount=530,
            payment_method='remittance'
        )
        payment_cash_lesson.save()

        self.stdout.write(self.style.SUCCESS('Успешное создание данных'))
