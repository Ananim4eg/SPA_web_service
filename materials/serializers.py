from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_forbidden_urls


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""
    video_url = serializers.URLField(validators=[validate_forbidden_urls],required=False)

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов"""
    lessons_count = serializers.SerializerMethodField()
    lessons_info = LessonSerializer(source='get_lesson',many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.get_lesson.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user,course=obj,is_active=True).exists()

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'preview_course', 'description', 'lessons_count', 'lessons_info', 'is_subscribed']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок на курсы"""
    course_name = serializers.CharField(source='course.course_name', read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['user']
