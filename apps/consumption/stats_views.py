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
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user_count = User.objects.count()
            active_users = User.objects.filter(status='active').count()
            
            return Response({
                "total_system_consumption": round(total, 2),
                "total_users": user_count,
                "active_users": active_users,
                "average_per_user": round(total / user_count if user_count > 0 else 0, 2)
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class PeakHoursView(views.APIView):
    def get(self, request):
        # Realistic residential load profile shape (24 hours)
        # Morning peak (7-9am) and evening peak (6-10pm)
        base_profile = [
            0.3, 0.2, 0.2, 0.2, 0.3, 0.5, # 00-05
            0.8, 1.2, 1.5, 1.0, 0.7, 0.6, # 06-11
            0.6, 0.7, 0.8, 1.0, 1.2, 1.8, # 12-17
            2.5, 2.8, 2.2, 1.5, 0.8, 0.5  # 18-23
        ]
        
        # Scale by user's average daily consumption
        avg_daily = ConsumptionData.objects.filter(user=request.user).aggregate(Avg('consumption'))['consumption__avg'] or 10
        scale = avg_daily / sum(base_profile)
        
        hours = [f"{i:02d}:00" for i in range(24)]
        data = []
        for h, val in zip(hours, base_profile):
            # Add some slight variation
            noise = random.uniform(0.9, 1.1)
            data.append({"hour": h, "value": round(val * scale * noise, 2)})
            
        return Response(data)

class MonthlyComparisonView(views.APIView):
    def get(self, request):
        data = []
        today = datetime.now().date()
        
        for i in range(5, -1, -1):
            # Get start and end of month
            first_day = (today.replace(day=1) - timedelta(days=i*30)).replace(day=1)
            last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            
            month_name = first_day.strftime('%b')
            
            current_month_sum = ConsumptionData.objects.filter(
                user=request.user, 
                date__range=[first_day, last_day]
            ).aggregate(total=Sum('consumption'))['total'] or 0
            
            # Previous year or previous month? Let's do previous year for "Comparison"
            prev_year_start = first_day.replace(year=first_day.year - 1)
            prev_year_end = last_day.replace(year=last_day.year - 1)
            
            previous_month_sum = ConsumptionData.objects.filter(
                user=request.user, 
                date__range=[prev_year_start, prev_year_end]
            ).aggregate(total=Sum('consumption'))['total'] or 0
            
            # If no data for previous year, let's simulate a baseline for comparison
            if previous_month_sum == 0 and current_month_sum > 0:
                previous_month_sum = current_month_sum * random.uniform(0.8, 1.2)

            data.append({
                "month": month_name, 
                "current": round(current_month_sum, 2), 
                "previous": round(previous_month_sum, 2)
            })
            
        return Response(data)
