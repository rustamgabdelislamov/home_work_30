from datetime import timedelta

from django.utils import timezone

from celery import shared_task

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from users.models import Subscribe, CustomUser


@shared_task
def update_course_or_lesson(course_id):
    """Отправляет уведомление на почту при обновлении курса"""
    emails = Subscribe.objects.filter(course=course_id).values_list('user__email', flat=True)
    emails = list(emails)
    send_mail(
            subject='Обновление',
            message='Курс обновлен',
            from_email=EMAIL_HOST_USER,
            recipient_list=emails
    )
    return emails

@shared_task
def last_login():
    """Проверяет последний вход пользователя"""

    users = CustomUser.objects.filter(last_login__isnull=False)
    for user in users:
        if timezone.now() > user.last_login + timedelta(days=30):
            user.is_active = False
            user.save()
