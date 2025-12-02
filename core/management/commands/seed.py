from django.core.management.base import BaseCommand
from faker import Faker
from core.models import CustomUser, Category, Idea, Comment, Vote
import random

class Command(BaseCommand):
    help = "Seed the database with users, categories, ideas, comments, and votes"

    def handle(self, *args, **options):
        fake = Faker()

        users = []
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
            users.append(user)

        category_names = ["Debate", "Technology", "Health", "Science", "Education"]
        categories = []
        for name in category_names:
            category, _ = Category.objects.get_or_create(name=name)
            categories.append(category)

        ideas = []
        for _ in range(20):
            author = random.choice(users)
            category = random.choice(categories)
            idea = Idea.objects.create(
                title=fake.sentence(),
                description=fake.text(max_nb_chars=200),
                author=author,
                category=category
            )
            ideas.append(idea)
        
        for _ in range(40):
            author = random.choice(users)
            idea = random.choice(ideas)
            Comment.objects.create(
                content=fake.text(max_nb_chars=100),
                author=author,
                idea=idea
            )

        for _ in range(40):
            user = random.choice(users)
            idea = random.choice(ideas)
            if not Vote.objects.filter(user=user, idea=idea).exists():
                Vote.objects.create(
                    user=user,
                    idea=idea
                )