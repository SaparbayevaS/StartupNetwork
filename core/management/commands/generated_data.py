from django.core.management.base import BaseCommand
from core.models import User, Category, Idea, IdeaCategory, Comment, Vote
from django.utils import timezone
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):
    help = "Generate sample data for testing (20 users, categories, ideas, comments, votes)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Deleting old data..."))
        Vote.objects.all().delete()
        Comment.objects.all().delete()
        IdeaCategory.objects.all().delete()
        Idea.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()


        users = []
        for _ in range(20):
            user = User.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                full_name=fake.name(),
                bio=fake.text(max_nb_chars=150),
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            users.append(user)
       

        categories = []
        for _ in range(20):
            cat = Category.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(max_nb_chars=200),
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            categories.append(cat)
      

        ideas = []
        for _ in range(20):
            idea = Idea.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.text(max_nb_chars=300),
                status=random.choice(["idea", "mvp", "investor_ready"]),
                author=random.choice(users),
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            ideas.append(idea)
       

        for idea in ideas:
            chosen_cats = random.sample(categories, k=random.randint(1, 3))
            for cat in chosen_cats:
                IdeaCategory.objects.create(idea=idea, category=cat)
        comments = []
        for _ in range(20):
            comment = Comment.objects.create(
                idea=random.choice(ideas),
                author=random.choice(users),
                content=fake.sentence(nb_words=15),
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            comments.append(comment)
        

        for _ in range(20):
            Vote.objects.create(
                idea=random.choice(ideas),
                user=random.choice(users),
                is_upvote=random.choice([True, False]),
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
       