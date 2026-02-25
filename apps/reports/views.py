from rest_framework import serializers, viewsets, views
from rest_framework.response import Response
from .models import Report
from django.http import HttpResponse
from apps.consumption.models import ConsumptionData
from django.db.models import Sum, Avg, Max, Count
from datetime import datetime, timedelta

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class DailyReportView(views.APIView):
    def get(self, request):
        user = request.user
        # Last 7 days daily summary
        days = []
        for i in range(6, -1, -1):
            date = datetime.now().date() - timedelta(days=i)
            stats = ConsumptionData.objects.filter(user=user, date=date).aggregate(
                total=Sum('consumption'),
                avg=Avg('consumption'),
                peak=Max('consumption'),
                devices=Count('device_name', distinct=True)
            )
            if stats['total']:
                days.append({
                    "period": date.strftime('%Y-%m-%d'),
                    "device_count": stats['devices'],
                    "total_consumption": round(stats['total'], 2),
                    "avg_daily": round(stats['avg'], 2),
                    "peak": round(stats['peak'], 2)
                })
        
        return Response({"type": "daily", "results": days})

class WeeklyReportView(views.APIView):
    def get(self, request):
        user = request.user
        # Last 4 weeks summary
        weeks = []
        today = datetime.now().date()
        for i in range(3, -1, -1):
            end_date = today - timedelta(days=today.weekday() + (i * 7))
            start_date = end_date - timedelta(days=6)
            
            stats = ConsumptionData.objects.filter(user=user, date__range=[start_date, end_date]).aggregate(
                total=Sum('consumption'),
                avg=Avg('consumption'),
                peak=Max('consumption'),
                devices=Count('device_name', distinct=True)
            )
            
            if stats['total']:
                weeks.append({
                    "period": f"Week {start_date.strftime('%d %b')} - {end_date.strftime('%d %b')}",
                    "device_count": stats['devices'],
                    "total_consumption": round(stats['total'], 2),
                    "avg_daily": round(stats['total'] / 7, 2),
                    "peak": round(stats['peak'], 2)
                })
        
        return Response({"type": "weekly", "results": weeks})

class MonthlyReportView(views.APIView):
    def get(self, request):
        user = request.user
        # Last 6 months summary
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
            
            stats = ConsumptionData.objects.filter(user=user, date__range=[first_day, last_day]).aggregate(
                total=Sum('consumption'),
                peak=Max('consumption'),
                devices=Count('device_name', distinct=True)
            )
            
            if stats['total']:
                months.append({
                    "period": first_day.strftime('%B %Y'),
                    "device_count": stats['devices'],
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
