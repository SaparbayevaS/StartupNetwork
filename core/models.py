from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class AbstactSoftDeletableModel(models.Model):
    is_deleted =models.BooleanField(default=False)
    deleted_at =models.DateTimeField(null=True,blank=True)
    
    def delete(self,using=None,keep_parents=False):
        self.is_deleted=True
        self.deleted_at=timezone.now()
        self.save(update_fields=['is_deleted','deleted_at'])
        
    def hard_delete(self,using=None,keep_parents=False):
        super().delete(using=using,keep_parents=keep_parents)
        
    class Meta:
        abstract=True
        

class UserProfile(AbstactSoftDeletableModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio=models.ImageField(upload_to='avatars/0',null=True,blank=True)
    
    total_likes=models.IntegerField(default=0)
    
    def __str__(self):
        return f'Profile: {self.user.username}'
    
    class Meta:
        verbose_name='User profile'
        verbose_name_plural='User profiles'
        
    
class Category(AbstactSoftDeletableModel):
    
    