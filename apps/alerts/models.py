from django.db import models
from django.conf import settings

class Alert(models.Model):
    ALERT_TYPES = (
        ('threshold', 'Threshold Limit'),
        ('abnormal', 'Abnormal Usage'),
        ('prediction', 'Predicted High Usage'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    threshold_value = models.FloatField(null=True, blank=True)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    status = models.CharField(max_length=10, default='unread')
    
    created_at = models.DateTimeField(auto_now_add=True)
