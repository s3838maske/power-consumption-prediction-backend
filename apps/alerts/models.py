from django.db import models
from django.conf import settings

class Alert(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('disabled', 'Disabled'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alerts')
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, null=True, blank=True)
    device_name = models.CharField(max_length=200, blank=True, null=True)
    threshold = models.FloatField(default=0.0)
    current_value = models.FloatField(default=0.0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.device_name or 'Global'} - {self.status}"
