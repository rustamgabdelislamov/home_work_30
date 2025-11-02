from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView)
from users.views import PaymentListAPIView, PaymentDestroyAPIView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register("", CourseViewSet, basename="courses")

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"),

    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/delete/<int:pk>/", PaymentDestroyAPIView.as_view(), name="payment_delete"),



] + router.urls

