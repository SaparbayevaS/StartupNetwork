from typing import Any, Type
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser, UserProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender: Type[CustomUser], instance: CustomUser, created: bool, **kwargs: Any) -> None:
    """
    Automatically create a UserProfile when a new CustomUser is created.
    """
    if created:
        UserProfile.objects.create(user=instance)
