from rest_framework import serializers, viewsets, views, status
from rest_framework.response import Response
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class SetThresholdView(views.APIView):
    def post(self, request):
        # Simulated logic
        return Response({"message": "Threshold set successfully"}, status=status.HTTP_200_OK)

class UpdateAlertView(views.APIView):
    def post(self, request):
        # Simulated logic
        return Response({"message": "Alert updated successfully"}, status=status.HTTP_200_OK)
