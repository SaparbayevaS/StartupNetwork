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
    name = models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name ='Category'
        verbose_name_plural='Categories'
        
READINESS_LEVELS=[
    ('idea','Только идея'),
    ('mvp','MVP'),
    ('investor_ready','Готов к инвесторам'),
]

class Idea(AbstactSoftDeletableModel):
    title=models.CharField(max_length=200)
    description=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='ideas')
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='ideas')
    readiness=models.CharField(max_length=20,choices=READINESS_LEVELS,default='idea')
    
    tags=models.ManyToManyField(Category,related_name='tagged_ideas',blank=True)
    logo=models.ImageField(upload_to='ideas/',null=True,blank=True)
    views=models.PositiveIntegerField(default=0)
    
    rating=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.title} ({self.author.username})'
    
    def update_rating(self):
        agg=self.votes.filter(is_deleted=False).aggregate(total=models.Sum('value'))
        total=agg['total'] or 0
        self.rating=int(total)
        self.save(update_fields=['rating'])
        
    def increment_views(self):
        self.views=models.F('views')+ 1
        self.save(update_fields=['views'])
        
    class Meta:
        ordering=['-rating','-created_at']
        verbose_name='Idea'
        verbose_name_plural='Ideas'
        
VOTE_CHOICES=[
    (1,'Like'),
    (-1,'Dislike'),
]

class Vote(AbstactSoftDeletableModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='votes')
    idea=models.ForeignKey(Idea,on_delete=models.CASCADE,related_name='votes')
    value=models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        
        constraints = [
            models.UniqueConstraint(fields=['user', 'idea'], name='unique_user_idea_vote')
        ]
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
    
    def clean(self):
        if self.value not in (1,-1):
            raise ValidationError('Invalid vote value')
        
    def save(self,*args,**kwargs):
        with transaction.atomic():
            is_update=bool(self.pk())
            super().save(*args,**kwargs)
            
            self.idea.update_rating()
            
            author_profile=getattr(self.idea.author,'profile',None)
            if author_profile:
                agg=Vote.objects.filter(idea__author=self.idea.author,value=1,is_deleted=False).aggregate(total=models.Count('id'))
                total_likes=agg['total'] or 0
                author_profile.total_likes=int(total_likes)
                author_profile.save(update_fields=['total_likes'])
                
    def delete(self,using=None,keep_parents=None):
        self.is_deleted=True
        self.deleted_at=timezone.now()
        self.save(update_fields=['is_deleted','deleted_at'])
        
        self.idea.update_rating()
        author_profile=getattr(self.idea.author,'profile',None)
        if author_profile:
            agg=Vote.objects.filter(idea__author=self.idea.author,value=1,is_deleted=False).aggregate(total=models.Count('id'))
            author_profile.total_likes=int(agg['total'] or 0)
            author_profile.save(update_fields=['total_likes'])
            
class Comment(AbstactSoftDeletableModel):
     idea=models.ForeignKey(Idea,on_delete=models.CASCADE,related_name='comments')
     author =models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
     content =models.TextField()
     parent =models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='replies')
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)
     
     def __str__(self):
         return f'Comment by {self.author.username} on {self.idea.title}'
     
     class Meta:
         ordering=['created_at']
         verbose_name='Comment'
         verbose_name_plural='Comments'


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_or_update_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if not hasattr(instance,'profile'):
            UserProfile.objects.create(user=instance)