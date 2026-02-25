from rest_framework import views, status
from rest_framework.response import Response
from .models import Device
from .serializers import DeviceSerializer
from apps.consumption.mongo_utils import get_mongo_collection
from bson import ObjectId
from datetime import datetime

class DeviceViewSet(views.APIView):
    def get(self, request):
        try:
            col = get_mongo_collection('devices_device')
            cursor = col.find({'user_id': request.user.id}).sort('created_at', -1)
            results = []
            for doc in cursor:
                results.append({
                    'id': str(doc.get('_id')),
                    'name': doc.get('name'),
                    'device_type': doc.get('device_type'),
                    'location': doc.get('location'),
                    'power_rating': doc.get('power_rating'),
                    'status': doc.get('status'),
                    'created_at': doc.get('created_at')
                })
            return Response(results)
        except Exception as e:
            import traceback
            print(f"DeviceViewSet GET error: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=500)

    def post(self, request):
        try:
            data = request.data
            col = get_mongo_collection('devices_device')
            
            # Simplified manual creation bypasses djongo/Django ORM
            new_device = {
                'user_id': request.user.id,
                'name': data.get('name'),
                'device_type': data.get('device_type'),
                'location': data.get('location', ''),
                'power_rating': float(data.get('power_rating', 0)),
                'status': data.get('status', 'active'),
                'created_at': datetime.now()
            }
            
            result = col.insert_one(new_device)
            new_device['id'] = str(result.inserted_id)
            del new_device['_id']
            
            return Response(new_device, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            print(f"DeviceViewSet POST error: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=500)

class DeviceDetailView(views.APIView):
    def delete(self, request, id):
        try:
            col = get_mongo_collection('devices_device')
            query = {'user_id': request.user.id}
            try:
                query['_id'] = ObjectId(id)
            except:
                return Response({'message': 'Invalid ID'}, status=400)

            result = col.delete_one(query)
            if result.deleted_count == 0:
                return Response({'message': 'Not found'}, status=404)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
