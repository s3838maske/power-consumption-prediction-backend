import pandas as pd
from rest_framework import views, status, parsers, generics
from rest_framework.response import Response
from .models import ConsumptionData
from .serializers import ConsumptionDataSerializer

class UploadConsumptionView(views.APIView):
    parser_classes = [parsers.MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Read Excel
            df = pd.read_excel(file)
            
            # Validation
            required = ['date', 'device', 'consumption']
            if not all(col in df.columns for col in required):
                return Response({'message': f'Missing columns. Required: {required}'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Parse and save
            data_objects = []
            for _, row in df.iterrows():
                data_objects.append(
                    ConsumptionData(
                        user=request.user,
                        device_name=row['device'],
                        category=row.get('category', 'General'),
                        date=pd.to_datetime(row['date']).date(),
                        consumption=float(row['consumption'])
                    )
                )
            
            ConsumptionData.objects.bulk_create(data_objects)
            
            return Response({'message': f'Successfully uploaded {len(data_objects)} records'}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConsumptionHistoryView(generics.ListAPIView):
    serializer_class = ConsumptionDataSerializer
    
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        return ConsumptionData.objects.filter(user=self.request.user)

class ConsumptionDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ConsumptionDataSerializer
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        return ConsumptionData.objects.filter(user=self.request.user)
