from rest_framework import serializers
from .models import ConsumptionData

class ConsumptionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumptionData
        fields = '__all__'
