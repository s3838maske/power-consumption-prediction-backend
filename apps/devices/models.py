from django.db import models
from apps.authentication.models import User

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True)
    power_rating = models.FloatField(default=0.0) # in Watts
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.device_type}) - {self.user.email}"
