from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

from users.models import Payment, CustomUser
from users.serializers import PaymentSerializer, CustomUserSerializer
from rest_framework.filters import OrderingFilter


class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class CustomUserListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("is_active",)
    ordering_fields = ("email",)


# class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUser.objects.all()
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_fields = ('is_active',)
#     ordering_fields = ('email',)


class CustomUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    # permission_classes = [IsOwnerOrStaff]


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
