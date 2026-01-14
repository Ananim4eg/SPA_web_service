from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_forbidden_urls


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_forbidden_urls])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons_info = LessonSerializer(source='get_lesson',many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.get_lesson.count()

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'preview_course', 'description', 'lessons_count', 'lessons_info']
