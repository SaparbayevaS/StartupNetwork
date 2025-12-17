from django.core.management.base import BaseCommand
from core.models import CustomUser, Category, Idea, IdeaCategory, Comment, Vote
from django.utils import timezone
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):
    """
    Django management command to generate sample data for testing

    Generates:20 users,20 categories,20 ideas and random comments and votes
    """
    help = "Generate sample data for testing (20 users, categories, ideas, comments, votes)"

    def handle(self, *args, **options):
        # Delete old data
        self.stdout.write(self.style.WARNING("Deleting old data..."))
        Vote.objects.all().delete()
        Comment.objects.all().delete()
        IdeaCategory.objects.all().delete()
        Idea.objects.all().delete()
        Category.objects.all().delete()
        CustomUser.objects.all().delete()

        # Create new users
        users = []
        for _ in range(20):
            user = CustomUser.objects.create_user(
                email=fake.email(),
                password="password123",
                full_name=fake.name(),
                bio=fake.text(max_nb_chars=150),
            )
            users.append(user)

        # Create a category
        categories = []
        for _ in range(20):
            cat = Category.objects.create(
                name=fake.word().capitalize()
            )
            categories.append(cat)

        # Create an idea
        ideas = []
        for _ in range(20):
            idea = Idea.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.text(max_nb_chars=300),
                author=random.choice(users),
            )
            ideas.append(idea)

        # Connect idea to category
        for idea in ideas:
            chosen_cats = random.sample(categories, k=random.randint(1, 3))
            for cat in chosen_cats:
                IdeaCategory.objects.create(idea=idea, category=cat)

        # Create comments
        for _ in range(20):
            Comment.objects.create(
                idea=random.choice(ideas),
                author=random.choice(users),
                content=fake.sentence(nb_words=15),
            )

        # Create votes
        for _ in range(20):
            Vote.objects.create(
                idea=random.choice(ideas),
                user=random.choice(users),
                is_upvote=random.choice([True, False]),
            )

        self.stdout.write(self.style.SUCCESS("Sample data generated successfully!"))