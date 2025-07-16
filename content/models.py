from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse


class TimelinePost(models.Model):
    POST_TYPE_CHOICES = [
        ('general', 'General'),
        ('catch_share', 'Catch Share'),
        ('education', 'Education'),
        ('tip', 'Tip'),
    ]
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timeline_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='general')
    image = models.CharField(max_length=255, blank=True)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class EducationalContent(models.Model):
    CATEGORY_CHOICES = [
        ('sustainability', 'Sustainability'),
        ('techniques', 'Fishing Techniques'),
        ('regulations', 'Regulations'),
        ('conservation', 'Conservation'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    # Updated to match the original educational_content model exactly
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    is_published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    read_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def get_absolute_url(self):
        return reverse('content:detail', kwargs={'content_id': self.pk})
    
    def increment_read_count(self):
        """Increment read count when content is viewed"""
        self.read_count += 1
        self.save(update_fields=['read_count'])
    
    class Meta:
        ordering = ['-featured', '-created_at']
        verbose_name = 'Educational Content'
        verbose_name_plural = 'Educational Content'


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(TimelinePost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'post']
