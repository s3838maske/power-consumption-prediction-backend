from rest_framework import serializers, viewsets, views, status, generics
from rest_framework.response import Response
from .models import Prediction
import random
from datetime import datetime, timedelta

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class GeneratePredictionView(views.APIView):
    def post(self, request):
        # Simulated generation
        return Response({
            "message": "Prediction generated successfully",
            "prediction": {
                "date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                "value": random.uniform(10, 50)
            }
        }, status=status.HTTP_201_CREATED)

class PredictionHistoryView(generics.ListAPIView):
    serializer_class = PredictionSerializer
    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

class CompareActualView(views.APIView):
    def get(self, request):
        # Simulating comparison data
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        data = [
            {"date": d, "predicted": random.uniform(20, 40), "actual": random.uniform(20, 40)}
            for d in dates
        ]
        return Response(data)

class PredictionByDeviceView(views.APIView):
    def get(self, request, device_id):
        # Filter predictions by device
        return Response({"device_id": device_id, "predictions": []})
