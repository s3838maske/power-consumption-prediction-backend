import pandas as pd
from rest_framework import views, status, parsers, generics
from rest_framework.response import Response
from .models import ConsumptionData
from .serializers import ConsumptionDataSerializer

from .mongo_utils import get_mongo_collection

class UploadConsumptionView(views.APIView):
    parser_classes = [parsers.MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Read Excel
            df = pd.read_excel(file)
            
            # Validation - be flexible with column names
            # Map common variations
            df.columns = [c.lower().strip() for c in df.columns]
            rename_map = {
                'device name': 'device',
                'device_name': 'device',
                'energy': 'consumption',
                'usage': 'consumption'
            }
            df = df.rename(columns=rename_map)
            
            required = ['date', 'device', 'consumption']
            if not all(col in df.columns for col in required):
                return Response({'message': f'Missing columns. Required: {required}. Found: {list(df.columns)}'}, status=status.HTTP_400_BAD_REQUEST)
            
            col = get_mongo_collection('consumption_consumptiondata')
            data_objects = []
            from datetime import datetime
            
            # Djongo enforces a unique index on 'id', so we must supply a unique integer for each raw document
            max_doc = col.find_one(sort=[("id", -1)])
            next_id = (max_doc.get("id", 0) or 0) + 1 if max_doc else 1
            
            for _, row in df.iterrows():
                try:
                    # Clean date parsing
                    dt = pd.to_datetime(row['date'])
                    mongo_date = datetime.combine(dt.date(), datetime.min.time())
                    
                    data_objects.append({
                        'id': next_id,
                        'user_id': request.user.id,
                        'device_name': str(row['device']),
                        'category': str(row.get('category', 'General')),
                        'date': mongo_date,
                        'consumption': float(row['consumption']),
                        'created_at': datetime.now()
                    })
                    next_id += 1
                except Exception as row_error:
                    print(f"Error parsing row: {row_error}")
                    continue
            
            if not data_objects:
                return Response({'message': 'No valid data found in file'}, status=status.HTTP_400_BAD_REQUEST)
                
            col.insert_many(data_objects)
            
            return Response({'message': f'Successfully uploaded {len(data_objects)} records'}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import traceback
            print(f"UploadConsumptionView error: {traceback.format_exc()}")
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from .mongo_utils import get_mongo_collection
from django.db.models import Sum
from bson import ObjectId

class ConsumptionHistoryView(views.APIView):
    def get(self, request):
        try:
            user = request.user
            col = get_mongo_collection('consumption_consumptiondata')
            
            # Fetch all records for user, sorted by date descending
            cursor = col.find({'user_id': user.id}).sort('date', -1)
            
            results = []
            for doc in cursor:
                results.append({
                    'id': str(doc.get('_id')),
                    'device_name': doc.get('device_name'),
                    'category': doc.get('category'),
                    'date': doc.get('date').strftime('%Y-%m-%d') if hasattr(doc.get('date'), 'strftime') else str(doc.get('date')),
                    'consumption': doc.get('consumption'),
                    'created_at': doc.get('created_at').strftime('%Y-%m-%d %H:%M:%S') if hasattr(doc.get('created_at'), 'strftime') else str(doc.get('created_at'))
                })
            
            return Response(results)
        except Exception as e:
            import traceback
            print(f"ConsumptionHistoryView error: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConsumptionDetailView(views.APIView):
    def get(self, request, id):
        try:
            col = get_mongo_collection('consumption_consumptiondata')
            # Try to find by _id (ObjectId) or by the integer id field if it exists
            query = {'user_id': request.user.id}
            try:
                query['_id'] = ObjectId(id)
            except:
                # If not a valid ObjectId, try as integer in the 'id' field
                try:
                    query['id'] = int(id)
                except:
                    return Response({'message': 'Invalid ID format'}, status=400)

            doc = col.find_one(query)
            if not doc:
                return Response({'message': 'Not found'}, status=404)
                
            return Response({
                'id': str(doc.get('_id')),
                'device_name': doc.get('device_name'),
                'category': doc.get('category'),
                'date': doc.get('date').strftime('%Y-%m-%d') if hasattr(doc.get('date'), 'strftime') else str(doc.get('date')),
                'consumption': doc.get('consumption'),
                'created_at': doc.get('created_at').strftime('%Y-%m-%d %H:%M:%S') if hasattr(doc.get('created_at'), 'strftime') else str(doc.get('created_at'))
            })
        except Exception as e:
            import traceback
            print(f"ConsumptionDetailView error: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            col = get_mongo_collection('consumption_consumptiondata')
            query = {'user_id': request.user.id}
            try:
                query['_id'] = ObjectId(id)
            except:
                try:
                    query['id'] = int(id)
                except:
                    return Response({'message': 'Invalid ID format'}, status=400)

            result = col.delete_one(query)
            if result.deleted_count == 0:
                return Response({'message': 'Not found'}, status=404)
                
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            import traceback
            print(f"ConsumptionDetailView delete error: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
