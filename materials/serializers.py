from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from users.models import Payment


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lessons(self, course):
        """Выводим количество уроков у курса по его идшнику"""
        return Lesson.objects.filter(course=course.id).count()


    def get_lessons(self, course):
        """Выводим уроки у курса по его идшнику"""
        return Lesson.objects.filter(course=course.id)

    class Meta:
        model = Course
        fields = ('name', 'description', 'count_lessons', 'lessons')

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
