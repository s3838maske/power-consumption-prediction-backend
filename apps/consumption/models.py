from django.db import models
from django.conf import settings

class ConsumptionData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    date = models.DateField()
    consumption = models.FloatField()  # kWh
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

