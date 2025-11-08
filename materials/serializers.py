from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import TitleLessonVideoUrlValidator
from users.models import Subscribe
from users.serializers import SubscribeSerializer


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return Subscribe.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(required=False, allow_blank=True, allow_null=True, validators=[TitleLessonVideoUrlValidator(field="video_url")])
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lessons(self, course):
        """Выводим количество уроков у курса по его идшнику"""
        return Lesson.objects.filter(course=course.id).count()

    class Meta:
        model = Course
        fields = ("name", "description", "count_lessons", "lessons")
