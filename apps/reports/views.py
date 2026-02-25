from rest_framework import serializers, viewsets, views
from rest_framework.response import Response
from .models import Report
from django.http import HttpResponse
from apps.consumption.models import ConsumptionData
from apps.consumption.mongo_utils import get_mongo_collection
from django.db.models import Sum, Avg, Max, Count
from datetime import datetime, timedelta

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class ReportViewSet(views.APIView):
    def get(self, request):
        try:
            col = get_mongo_collection('reports_report')
            cursor = col.find({'user_id': request.user.id}).sort('generated_at', -1)
            results = []
            for doc in cursor:
                results.append({
                    'id': str(doc.get('_id')),
                    'report_type': doc.get('report_type'),
                    'file_path': doc.get('file_path'),
                    'generated_at': doc.get('generated_at').strftime('%Y-%m-%d %H:%M:%S') if hasattr(doc.get('generated_at'), 'strftime') else str(doc.get('generated_at'))
                })
            return Response(results)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class DailyReportView(views.APIView):
    def get(self, request):
        user = request.user
        col = get_mongo_collection('consumption_consumptiondata')
        user_id = user.id
        
        days = []
        for i in range(6, -1, -1):
            date_obj = datetime.now().date() - timedelta(days=i)
            # Create range for being safe with time portions
            start_dt = datetime.combine(date_obj, datetime.min.time())
            end_dt = datetime.combine(date_obj, datetime.max.time())
            
            pipeline = [
                {'$match': {'user_id': user_id, 'date': {'$gte': start_dt, '$lte': end_dt}}},
                {'$group': {
                    '_id': None,
                    'total': {'$sum': '$consumption'},
                    'avg': {'$avg': '$consumption'},
                    'peak': {'$max': '$consumption'},
                    'devices': {'$addToSet': '$device_name'}
                }}
            ]
            result = list(col.aggregate(pipeline))
            stats = result[0] if result else None
            
            if stats and stats['total']:
                days.append({
                    "period": date_obj.strftime('%Y-%m-%d'),
                    "device_count": len(stats['devices']),
                    "total_consumption": round(stats['total'], 2),
                    "avg_daily": round(stats['avg'], 2),
                    "peak": round(stats['peak'], 2)
                })
        
        return Response({"type": "daily", "results": days})

class WeeklyReportView(views.APIView):
    def get(self, request):
        user = request.user
        col = get_mongo_collection('consumption_consumptiondata')
        user_id = user.id
        
        weeks = []
        today = datetime.now().date()
        for i in range(3, -1, -1):
            end_date = today - timedelta(days=today.weekday() + (i * 7))
            start_date = end_date - timedelta(days=6)
            
            start_dt = datetime.combine(start_date, datetime.min.time())
            end_dt = datetime.combine(end_date, datetime.max.time())
            
            pipeline = [
                {'$match': {'user_id': user_id, 'date': {'$gte': start_dt, '$lte': end_dt}}},
                {'$group': {
                    '_id': None,
                    'total': {'$sum': '$consumption'},
                    'avg': {'$avg': '$consumption'},
                    'peak': {'$max': '$consumption'},
                    'devices': {'$addToSet': '$device_name'}
                }}
            ]
            result = list(col.aggregate(pipeline))
            stats = result[0] if result else None
            
            if stats and stats['total']:
                weeks.append({
                    "period": f"Week {start_date.strftime('%d %b')} - {end_date.strftime('%d %b')}",
                    "device_count": len(stats['devices']),
                    "total_consumption": round(stats['total'], 2),
                    "avg_daily": round(stats['total'] / 7, 2),
                    "peak": round(stats['peak'], 2)
                })
        
        return Response({"type": "weekly", "results": weeks})

class MonthlyReportView(views.APIView):
    def get(self, request):
        user = request.user
        col = get_mongo_collection('consumption_consumptiondata')
        user_id = user.id
        
        months = []
        today = datetime.now().date()
        for i in range(5, -1, -1):
            # First day of month
            first_day = (today.replace(day=1) - timedelta(days=i*30)).replace(day=1)
            # Last day of month
            if first_day.month == 12:
                next_month = first_day.replace(year=first_day.year + 1, month=1, day=1)
            else:
                next_month = first_day.replace(month=first_day.month + 1, day=1)
            last_day = next_month - timedelta(days=1)
            
            start_dt = datetime.combine(first_day, datetime.min.time())
            end_dt = datetime.combine(last_day, datetime.max.time())
            
            pipeline = [
                {'$match': {'user_id': user_id, 'date': {'$gte': start_dt, '$lte': end_dt}}},
                {'$group': {
                    '_id': None,
                    'total': {'$sum': '$consumption'},
                    'peak': {'$max': '$consumption'},
                    'devices': {'$addToSet': '$device_name'}
                }}
            ]
            result = list(col.aggregate(pipeline))
            stats = result[0] if result else None
            
            if stats and stats['total']:
                months.append({
                    "period": first_day.strftime('%B %Y'),
                    "device_count": len(stats['devices']),
                    "total_consumption": round(stats['total'], 2),
                    "avg_daily": round(stats['total'] / 30, 2),
                    "peak": round(stats['peak'], 2)
                })
        
        return Response({"type": "monthly", "results": months})

class DownloadExcelReportView(views.APIView):
    def get(self, request):
        # Placeholder for excel download
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
        return response

class DownloadPdfReportView(views.APIView):
    def get(self, request):
        # Placeholder for pdf download
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response
