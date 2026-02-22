from django.db import models
from django.conf import settings

class Report(models.Model):
    REPORT_TYPES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    file_path = models.CharField(max_length=255)
    generated_at = models.DateTimeField(auto_now_add=True)
