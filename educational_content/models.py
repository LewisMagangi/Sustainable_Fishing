from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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
    
    # Exact fields from database_schema.dbml
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
        return reverse('educational_content:detail', kwargs={'content_id': self.pk})
    
    def increment_read_count(self):
        """Increment read count when content is viewed"""
        self.read_count += 1
        self.save(update_fields=['read_count'])
    
    class Meta:
        ordering = ['-featured', '-created_at']
        verbose_name = 'Educational Content'
        verbose_name_plural = 'Educational Content'
