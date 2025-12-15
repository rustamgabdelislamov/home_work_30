
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson
from materials.paginators import MaterialsPaginator
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)
from users.models import Subscribe
from users.permissions import IsModer, IsOwner
from users.tasks import update_course_or_lesson


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = serializer.instance # serializer.instance возвращает текущий экземпляр объекта, который будет обновлён
        changed = False # флаг
        # print(instance.__dict__)

        for attr, new_value in serializer.validated_data.items(): # serializer.validated_data содержит данные,
            # которые были отправлены в запросе и проверены сериализатором. Цикл проходит по каждому атрибуту и
            # новому значению
            old_value = getattr(instance, attr, None)

            if old_value != new_value: #  возвращает текущее значение атрибута объекта. Если атрибут не существует, # возвращается None
                changed =True
                break
        instance = serializer.save() # сохраняет обновлённые данные в базе данных
        if changed :
            course_id = getattr(instance, "id", None) # getattr(instance, "id", None) возвращает ID курса
            update_course_or_lesson.delay(course_id=course_id) # Если были внесены изменения, вызывается задача
            # update_course_or_lesson с ID курса.


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        user = self.request.user
        qs = Lesson.objects.all()
        if not user.is_authenticated:
            return Lesson.objects.none()
        # проверка на группу "moders"
        is_moder = user.groups.filter(name='moders').exists()
        if user.is_staff or user.is_superuser or is_moder:
            return qs
        return qs.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
