from rest_framework import serializers


from users.models import Payment, CustomUser, Subscribe


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class ClassModerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "id")


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = ("id", "user", "course")

