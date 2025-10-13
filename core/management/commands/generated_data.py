from django.core.management.base import BaseCommand
from core.models import User, Category, Idea, IdeaCategory, Comment
import random

class Command(BaseCommand):
    help = "Generate simple data"

    def handle(self, *args, **options):
        User.objects.all().delete()
        Category.objects.all().delete()
        Idea.objects.all().delete()
        Comment.objects.all().delete()

        users = [
            User.objects.create(username = f"user{i}", email = f"user{i}@mail.com", full_name = f"User {i}")
            for i in range(5)
        ]

        categories = [
            Category.objects.create(name = f"Category {i}", description = f"Description {i}")
            for i in range(3)
        ]

        for i in range(10):
            idea = Idea.objects.create(
                title = f"Idea {i}",
                description = f"Description for idea {i}",
                status = "open",
                author = random.choice(users),
            )
            idea.categories.add(*random.sample(categories, k=random.randint(1, len(categories))))

        self.stdout.write(self.style.SUCCESS("Data generated successfully!"))