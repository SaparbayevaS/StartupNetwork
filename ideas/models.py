from django.db.models import CharField, TextField, ForeignKey, CASCADE

from common.models import AbstactSoftDeletableModel
from common.constants import CATEGORY_NAME_MAX_LENGTH, IDEA_TITLE_MAX_LENGTH
from users.models import CustomUser

class Category(AbstactSoftDeletableModel):
    """
    Category for ideas.
    """
    name = CharField(max_length=CATEGORY_NAME_MAX_LENGTH)

    def __str__(self) -> str:
        return self.name


class Idea(AbstactSoftDeletableModel):
    """
    Idea model.
    Contains title, description, category and author.
    """
    title = CharField(max_length=IDEA_TITLE_MAX_LENGTH)
    description = TextField()
    category = ForeignKey(Category, on_delete=CASCADE, related_name='ideas')
    author = ForeignKey(CustomUser, on_delete=CASCADE, related_name='ideas')

    def __str__(self) -> str:
        return self.title


class Comment(AbstactSoftDeletableModel):
    """
    Comment model for ideas.
    """
    idea = ForeignKey(Idea, on_delete=CASCADE, related_name='comments')
    author = ForeignKey(CustomUser, on_delete=CASCADE, related_name='comments')
    content = TextField()


class Vote(AbstactSoftDeletableModel):
    """
    Vote model.
    ONe user can only vote for one idea.
    """
    idea = ForeignKey(Idea, on_delete=CASCADE, related_name='votes')
    user = ForeignKey(CustomUser, on_delete=CASCADE, related_name='votes')

    class Meta:
        unique_together = ('idea', 'user')