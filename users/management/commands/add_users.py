from django.core.management import BaseCommand

from materials.models import Course
from users.models import CustomUser, Payment


class Command(BaseCommand):
    help = "Create 3 sample users and 3 sample payments"

    def handle(self, *args, **options):
        users = []

        users_data = [
            {
                "email": "alice@example.com",
                "password": "password123",
                "phone_number": "+79990000001",
                "city": "Москва",
            },
            {
                "email": "bob@example.com",
                "password": "password123",
                "phone_number": "+79990000002",
                "city": "Санкт-Петербург",
            },
            {
                "email": "carol@example.com",
                "password": "password123",
                "phone_number": "+79990000003",
                "city": "Екатеринбург",
            },
        ]

        for user in users_data:
            user, created = CustomUser.objects.get_or_create(**user)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added user: {user.email}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"User already exists: {user.email}")
                )
            users.append(user)

        course = list(Course.objects.all()[:3])
        payments_data = [
            {
                "user": users[0],
                "date": "2024-10-01",
                "payment_course": course[0],
                "amount": 100,
                "payment_method": "cash",
            },
            {
                "user": users[1],
                "date": "2024-10-02",
                "payment_course": course[1],
                "amount": 200,
                "payment_method": "translation",
            },
            {
                "user": users[2],
                "date": "2024-10-03",
                "payment_course": course[2],
                "amount": 300,
                "payment_method": "cash",
            },
        ]

        for payment in payments_data:
            payment, created = Payment.objects.get_or_create(**payment)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added book: {payment.payment_course}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Book already exists: {payment.payment_course}")
                )
