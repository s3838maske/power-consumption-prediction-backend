from django.db import models
from django.conf import settings

class Prediction(models.Model):
    TYPE_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    predicted_value = models.FloatField()
    actual_value = models.FloatField(null=True, blank=True)
    mae = models.FloatField(null=True, blank=True)
    rmse = models.FloatField(null=True, blank=True)
    model_used = models.CharField(max_length=50)
    target_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-target_date']
