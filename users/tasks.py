from celery import shared_task

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from users.models import Subscribe


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
