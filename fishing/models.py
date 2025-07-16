from django.db import models
from django.conf import settings
from django.urls import reverse


class Catch(models.Model):
    STATUS_CHOICES = [
        ('unsold', 'Unsold'),
        ('sold', 'Sold'),
        ('donated', 'Donated'),
    ]
    
    # Using the exact structure from catches app
    fisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fish_type = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=100)
    catch_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unsold')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.fish_type} - {self.weight}kg by {self.fisher.username}"
    
    def get_absolute_url(self):
        return reverse('fishing:catch_detail', kwargs={'catch_id': self.pk})
    
    class Meta:
        ordering = ['-catch_date', '-created_at']
        verbose_name = 'Catch'
        verbose_name_plural = 'Catches'
