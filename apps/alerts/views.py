from rest_framework import serializers, viewsets, views, status
from rest_framework.response import Response
from .models import Alert

from django.db.models import Sum
from apps.consumption.models import ConsumptionData
from apps.consumption.mongo_utils import get_mongo_collection
from datetime import datetime, timedelta
from bson import ObjectId
import traceback

class AlertSerializer(serializers.ModelSerializer):
    current_value = serializers.SerializerMethodField()
    is_triggered = serializers.SerializerMethodField()

    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['user']

    def get_current_value(self, obj):
        # We need to handle both Model objects and dictionary-like objects from pymongo
        device_name = getattr(obj, 'device_name', None) or obj.get('device_name')
        user_id = getattr(obj, 'user_id', None) or obj.get('user_id')
        
        if device_name and user_id:
            last_30_days = datetime.now() - timedelta(days=30)
            col = get_mongo_collection('consumption_consumptiondata')
            
            pipeline = [
                {'$match': {
                    'user_id': user_id,
                    'device_name': device_name,
                    'date': {'$gte': last_30_days}
                }},
                {'$group': {'_id': None, 'total': {'$sum': '$consumption'}}}
            ]
            result = list(col.aggregate(pipeline))
            total = result[0]['total'] if result else 0
            return round(total, 2)
        return 0

    def get_is_triggered(self, obj):
        current = self.get_current_value(obj)
        threshold = getattr(obj, 'threshold', 0) or obj.get('threshold', 0)
        status = getattr(obj, 'status', 'active') or obj.get('status', 'active')
        return current > threshold if status != 'disabled' else False

class AlertViewSet(views.APIView):
    def get(self, request, id=None):
        try:
            col = get_mongo_collection('alerts_alert')
            cursor = col.find({'user_id': request.user.id}).sort('created_at', -1)
            results = []
            for doc in cursor:
                # Calculate current_value and is_triggered manually for speed/reliablity
                current_val = 0
                device_name = doc.get('device_name')
                if device_name:
                    last_30_days = datetime.now() - timedelta(days=30)
                    col_cons = get_mongo_collection('consumption_consumptiondata')
                    p = [
                        {'$match': {'user_id': request.user.id, 'device_name': device_name, 'date': {'$gte': last_30_days}}},
                        {'$group': {'_id': None, 'total': {'$sum': '$consumption'}}}
                    ]
                    res = list(col_cons.aggregate(p))
                    current_val = res[0]['total'] if res else 0

                results.append({
                    'id': str(doc.get('_id')),
                    'device_name': doc.get('device_name'),
                    'threshold': doc.get('threshold'),
                    'current_value': round(current_val, 2),
                    'is_triggered': (current_val > doc.get('threshold', 0)) if doc.get('status') != 'disabled' else False,
                    'status': doc.get('status'),
                    'message': doc.get('message'),
                    'created_at': doc.get('created_at').strftime('%Y-%m-%d %H:%M:%S') if hasattr(doc.get('created_at'), 'strftime') else str(doc.get('created_at'))
                })
            return Response(results)
        except Exception as e:
            import traceback
            print(f"AlertViewSet GET error: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=500)

    def delete(self, request, id):
        try:
            col = get_mongo_collection('alerts_alert')
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

class SetThresholdView(views.APIView):
    def post(self, request):
        try:
            user_id = request.user.id
            device_id_str = request.data.get('device_id')
            threshold = float(request.data.get('threshold', 0))
            
            if not device_id_str:
                return Response({"error": "device_id is required"}, status=400)
            
            # Fetch device name using pymongo
            col_dev = get_mongo_collection('devices_device')
            try:
                dev_doc = col_dev.find_one({'_id': ObjectId(device_id_str), 'user_id': user_id})
            except:
                return Response({"error": "Invalid device_id"}, status=400)
                
            if not dev_doc:
                return Response({"error": "Device not found"}, status=404)
            
            device_name = dev_doc.get('name')
            
            col_alert = get_mongo_collection('alerts_alert')
            # Check if exists
            existing = col_alert.find_one({'user_id': user_id, 'device_name': device_name})
            
            if existing:
                col_alert.update_one(
                    {'_id': existing['_id']},
                    {'$set': {'threshold': threshold, 'status': 'active'}}
                )
                alert_id = existing['_id']
            else:
                new_alert = {
                    'user_id': user_id,
                    'device_name': device_name,
                    'threshold': threshold,
                    'current_value': 0.0,
                    'status': 'active',
                    'message': f"Alert for {device_name}",
                    'created_at': datetime.now()
                }
                res = col_alert.insert_one(new_alert)
                alert_id = res.inserted_id
            
            return Response({"message": "Threshold set successfully", "id": str(alert_id)}, status=201)
        except Exception as e:
            import traceback
            print(f"SetThresholdView error: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=500)

class UpdateAlertView(views.APIView):
    def post(self, request):
        try:
            alert_id_str = request.data.get('alert_id')
            status_val = request.data.get('status')
            
            col = get_mongo_collection('alerts_alert')
            try:
                oid = ObjectId(alert_id_str)
            except:
                return Response({"error": "Invalid alert_id"}, status=400)
                
            result = col.update_one(
                {'_id': oid, 'user_id': request.user.id},
                {'$set': {'status': status_val}}
            )
            
            if result.matched_count == 0:
                return Response({"error": "Alert not found"}, status=404)
                
            return Response({"message": "Alert updated successfully"})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
