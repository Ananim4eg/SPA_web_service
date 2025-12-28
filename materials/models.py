from django.db import models


class Course(models.Model):
    """Модель курса"""
    course_name = models.CharField(max_length=100, verbose_name="название курса")
    preview_course = models.ImageField(upload_to='preview/', verbose_name='превью курса', null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='описание')

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    """Модель урока"""
    lesson_name = models.CharField(max_length=100, verbose_name="название урока")
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    preview_lesson = models.ImageField(upload_to='preview/', verbose_name='превью урока', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
