from django.db.models import Sum, Avg, Max
from rest_framework import views
from rest_framework.response import Response
from .models import ConsumptionData
from datetime import datetime, timedelta
import random

class DashboardStatsView(views.APIView):
    def get(self, request):
        user = request.user
        print(f"DEBUG: Request User: {user.email}, ID: {user.id}")
        last_30_days = datetime.now() - timedelta(days=30)
        
        try:
            # Aggregate stats
            stats = ConsumptionData.objects.filter(user=user, date__gte=last_30_days).aggregate(
                total=Sum('consumption'),
                avg=Avg('consumption'),
                peak=Max('consumption')
            )
            
            # Device breakdown
            device_breakdown = list(ConsumptionData.objects.filter(user=user, date__gte=last_30_days).values('device_name').annotate(
                consumption=Sum('consumption')
            ).order_by('-consumption'))
            
            # Daily usage for line chart
            daily_usage = list(ConsumptionData.objects.filter(user=user, date__gte=last_30_days).values('date').annotate(
                consumption=Sum('consumption')
            ).order_by('date'))

            avg_val = stats.get('avg') or 0

            return Response({
                'totalConsumption': stats.get('total') or 0,
                'avgDailyConsumption': avg_val,
                'peakConsumption': stats.get('peak') or 0,
                'predictedNextMonth': avg_val * 30, # Simple baseline prediction
                'deviceBreakdown': [{'deviceName': d['device_name'], 'consumption': d['consumption']} for d in device_breakdown],
                'dailyData': [{'date': d['date'].strftime('%Y-%m-%d'), 'consumption': d['consumption']} for d in daily_usage]
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class UserSummaryView(views.APIView):
    def get(self, request):
        # Simulated or aggregated user summary
        user = request.user
        try:
            total = ConsumptionData.objects.filter(user=user).aggregate(total=Sum('consumption'))['total'] or 0
            device_count = ConsumptionData.objects.filter(user=user).values('device_name').distinct().count()
            return Response({
                "total_consumption": total,
                "average_daily": total / 30 if total > 0 else 0,
                "active_devices": device_count
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class AdminSummaryView(views.APIView):
    def get(self, request):
        if request.user.role != 'admin':
            return Response({"error": "Unauthorized"}, status=403)
        
        try:
            total = ConsumptionData.objects.aggregate(total=Sum('consumption'))['total'] or 0
            user_count = User.objects.count()
            return Response({
                "total_system_consumption": total,
                "total_users": user_count,
                "average_per_user": total / user_count if user_count > 0 else 0
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class PeakHoursView(views.APIView):
    def get(self, request):
        # In a real app, you'd need hourly data. Simulating for now.
        hours = [f"{i:02d}:00" for i in range(24)]
        values = [random.randint(10, 100) for _ in range(24)]
        return Response([{"hour": h, "value": v} for h, v in zip(hours, values)])

class MonthlyComparisonView(views.APIView):
    def get(self, request):
        # Simulating monthly data
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        current = [random.randint(200, 500) for _ in range(6)]
        previous = [random.randint(200, 500) for _ in range(6)]
        return Response([{"month": m, "current": c, "previous": p} for m, c, p in zip(months, current, previous)])
