from typing import Any, Type
from django.db.models.signals import post_save
from django.dispatch import receiver

from ideas.models import Idea, Comment, Vote

@receiver(post_save, sender=Idea)
def update_user_idea_count(sender: Type[Idea], instance: Idea, created: bool, **kwargs: Any) -> None:
    """
    Increment the total_ideas count on the author's profile
    when a new idea is created.
    """
    profile = instance.author.profile
    if created:
        profile.total_ideas += 1
        profile.save(update_fields=['total_ideas'])


@receiver(post_save, sender=Comment)
def update_user_comment_count(sender: Type[Comment], instance: Comment, created: bool, **kwargs: Any) -> None:
    """
    Increment the total_comments count on the author's profile
    when a new comment is created.
    """
    profile = instance.author.profile
    if created:
        profile.total_comments += 1
        profile.save(update_fields=['total_comments'])


@receiver(post_save, sender=Vote)
def update_user_vote_count(sender: Type[Vote], instance: Vote, created: bool, **kwargs: Any) -> None:
    """
    Increment the total_votes count on the user's profile
    when a new vote is created.
    """
    profile = instance.user.profile
    if created:
        profile.total_votes += 1
        profile.save(update_fields=['total_votes'])
