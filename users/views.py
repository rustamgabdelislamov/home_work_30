from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.models import Payment, CustomUser, Subscribe
from users.serializers import (
    PaymentSerializer,
    CustomUserSerializer,
    ClassModerSerializer,
)
from rest_framework.filters import OrderingFilter

from users.services import create_stripe_payment, create_stripe_session


class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class CustomUserListAPIView(generics.ListAPIView):
    serializer_class = ClassModerSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("is_active",)
    ordering_fields = ("email",)


class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClassModerSerializer

    def get_serializer_class(self):
        # Получаем объект пользователя
        obj = self.get_object()
        if self.request.user == obj:
            return CustomUserSerializer  # полный сериализатор для владельца
        return super().get_serializer_class()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("is_active",)
    ordering_fields = ("email",)


class CustomUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class CustomUserDestroyAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("payment_course", "payment_lesson", "payment_method")
    ordering_fields = ("date",)


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payment.objects.all()


class SubscribeAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscribe.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()  # отписываем (удаляем все найденные)
            return Response({"message": "отписано"})
        else:
            Subscribe.objects.create(user=user, course=course_item)  # подписываем
            return Response({"message": "подписано"})


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


    def perform_create(self, serializer):
        print(f"User: {self.request.user}")  # Вывод текущего пользователя
        print(f"Is Authenticated: {self.request.user.is_authenticated}")
        payment = serializer.save(user=self.request.user) # берем user

        amount = payment.amount # создаем сумму
        price = create_stripe_payment(amount) # создаем стоимость
        session_id, link = create_stripe_session(price) # создаем сессию
        payment.session_id = session_id # сохраняем данные в поля модели
        payment.link = link  # сохраняем данные в поля модели
        payment.save()