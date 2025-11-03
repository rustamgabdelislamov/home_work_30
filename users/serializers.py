from rest_framework import serializers

from materials.serializers import LessonSerializer
from users.models import Payment, CustomUser


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "id", "is_staff", "phone_number", "image", "city")


# class CustomUserDetailSerializer(serializers.ModelSerializer):
#     lessons = LessonSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'lessons')


# class CustomUserIsOwnerDetailSerializer(serializers.ModelSerializer):
#     lessons = LessonSerializer(many=True, read_only=True)
#
#
#     class Meta:
#         model = CustomUser
#         fields = '__all__'
