from django.db import models
from django.utils import timezone
from django.conf import settings


class Catch(models.Model):
    STATUS_CHOICES = [
        ('sold', 'Sold'),
        ('unsold', 'Unsold'),
        ('donated', 'Donated'),
    ]
    
    fisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='catches')
    fish_type = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=100)
    catch_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unsold')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
