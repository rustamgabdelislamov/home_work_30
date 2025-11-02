from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Payment
from users.serializer import PaymentSerializer
from rest_framework.filters import OrderingFilter


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('payment_course', 'payment_lesson', 'payment_method')
    ordering_fields = ('date',)


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
