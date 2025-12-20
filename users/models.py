from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from materials.models import Course, Lesson


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите email"
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Необязательное поле. Введите номер телефона",
    )
    image = models.ImageField(
        upload_to="users/image", verbose_name="Фото", blank=True, null=True
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Необязательное поле. Введите город",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активность",
        blank=True,
        null=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [("cash", "наличные"), ("translation", "перевод")]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    payment_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course",
        verbose_name="Оплата курса",
        blank=True,
        null=True,
    )
    payment_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="lesson",
        verbose_name="Оплата урока",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=12,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
        blank=True,
        null=True,
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
    )
    link = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка сессии",
    )

    def __str__(self):
        return f"{self.user} {self.payment_course if self.payment_course else self.payment_lesson} {self.amount}"

    class Meta:
        verbose_name = "оплата"
        verbose_name_plural = "оплаты"


class Subscribe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscribe",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscribe_course",
        verbose_name="подписка на курс",
        blank=True,
        null=True,
    )
