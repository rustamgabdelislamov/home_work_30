from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()

    def get_count_lessons(self, course):
        """Выводим количество уроков у курса по его идшнику"""
        return Lesson.objects.filter(course=course.id).count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'count_lessons')

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
