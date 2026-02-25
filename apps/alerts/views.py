from rest_framework import serializers, viewsets, views, status
from rest_framework.response import Response
from .models import Alert

from django.db.models import Sum
from apps.consumption.models import ConsumptionData
from datetime import datetime, timedelta

class AlertSerializer(serializers.ModelSerializer):
    current_value = serializers.SerializerMethodField()
    is_triggered = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['user']

    def get_current_value(self, obj):
        if obj.device:
            last_30_days = datetime.now() - timedelta(days=30)
            total = ConsumptionData.objects.filter(
                user=obj.user, 
                device_name=obj.device.name,
                date__gte=last_30_days
            ).aggregate(total=Sum('consumption'))['total'] or 0
            return round(total, 2)
        return obj.current_value

    def get_is_triggered(self, obj):
        current = self.get_current_value(obj)
        return current > obj.threshold if obj.status != 'disabled' else False

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

from apps.devices.models import Device

class SetThresholdView(views.APIView):
    def post(self, request):
        user = request.user
        device_id = request.data.get('device_id')
        threshold = request.data.get('threshold')
        
        if not device_id or not threshold:
            return Response({"error": "device_id and threshold are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            device = Device.objects.get(id=device_id, user=user)
        except Device.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Check if alert already exists for this device
        alert, created = Alert.objects.get_or_create(
            user=user,
            device=device,
            defaults={
                'device_name': device.name,
                'threshold': float(threshold),
                'status': 'active'
            }
        )
        
        if not created:
            alert.threshold = float(threshold)
            alert.status = 'active'
            alert.save()
            
        return Response(AlertSerializer(alert).data, status=status.HTTP_201_CREATED)

class UpdateAlertView(views.APIView):
    def post(self, request):
        alert_id = request.data.get('alert_id')
        status_val = request.data.get('status')
        
        try:
            alert = Alert.objects.get(id=alert_id, user=request.user)
            alert.status = status_val
            alert.save()
            return Response(AlertSerializer(alert).data)
        except Alert.DoesNotExist:
            return Response({"error": "Alert not found"}, status=status.HTTP_404_NOT_FOUND)
