from django.db.models import Model, DateTimeField
from django.utils import timezone

class AbstactSoftDeletableModel(Model):
    """
    Base model for soft delete.
    Contains created, updated, deleted time fields.
    """
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    deleted_at = DateTimeField(null=True, blank=True)

    def delete(self, using: str = None, keep_parents: bool = False) -> None:
        """
        Marks object as deleted by setting deleted_at time.
        """
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    class Meta:
        abstract = True