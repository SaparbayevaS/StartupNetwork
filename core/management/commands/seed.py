from django.core.management.base import BaseCommand
from faker import Faker
from core.models import CustomUser

class Command(BaseCommand):
    help = "Seed the database with 20 users"

    def handle(self, *args, **options):
        fake = Faker()
        self.stdout.write("Seeding data...")

        for _ in range(20):
            email = fake.unique.email()
            full_name = fake.name()
            bio = fake.text(max_nb_chars=200)
            password = "password123"

            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                bio=bio
            )
            self.stdout.write(self.style.SUCCESS(f"Created user {email}"))

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
