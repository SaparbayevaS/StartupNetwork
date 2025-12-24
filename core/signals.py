from typing import Any, Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, UserProfile, Idea, Comment, Vote

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender: Type[CustomUser], instance: CustomUser, created: bool, **kwargs: Any) -> None:
    """
    Create a userProfile automatically when a new CustomUser is created
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=Idea)
def update_user_idea_count(sender: Type[Idea], instance: Idea, created: bool, **kwargs: Any) -> None:
    """
    Increment the total_ideas count on the authors profile
    when a new idea is created
    """
    profile = instance.author.profile
    if created:
        profile.total_ideas += 1
        profile.save(update_fields=['total_ideas'])

@receiver(post_save, sender=Comment)
def update_user_comment_count(sender: Type[Comment], instance: Comment, created: bool, **kwargs: Any) -> None:
    """
    Increment the total_comments count on the authors profile
    when a new comment is created
    """
    profile = instance.author.profile
    if created:
        profile.total_comments += 1
        profile.save(update_fields=['total_comments'])

@receiver(post_save, sender=Vote)
def update_user_vote_count(sender: Type[Vote], instance: Vote, created: bool, **kwargs: Any) -> None:
    """
    Increment the total_votes count on the users profile
    when a new vote is created
    """
    profile = instance.user.profile
    if created:
        profile.total_votes += 1
        profile.save(update_fields=['total_votes'])