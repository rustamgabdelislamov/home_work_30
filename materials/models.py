from django.db import models
from config import settings


class Course(models.Model):
    name = models.CharField(
        unique=True,
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название текста",
    )
    preview = models.ImageField(
        upload_to="materials/preview", verbose_name="Превью", blank=True, null=True
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание курса",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="courses",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    name = models.CharField(
        unique=True,
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание урока",
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    preview = models.ImageField(
        upload_to="materials/preview", verbose_name="Превью", blank=True, null=True
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="lessons",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
