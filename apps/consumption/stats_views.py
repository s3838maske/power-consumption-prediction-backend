from django.db.models import Sum, Avg, Max
from django.conf import settings
from rest_framework import views
from rest_framework.response import Response
from .models import ConsumptionData
from .mongo_utils import get_mongo_collection
from datetime import datetime, timedelta, date
import random


def format_date(d):
    """Safely convert date / datetime / string to YYYY-MM-DD string."""
    if isinstance(d, str):
        return d[:10]
    if hasattr(d, 'strftime'):
        return d.strftime('%Y-%m-%d')
    return str(d)[:10]


class DashboardStatsView(views.APIView):
    def get(self, request):
        user = request.user
        # Use .date() so comparison works correctly with DateField
        last_30_days = datetime.now().date() - timedelta(days=30)
        # Convert to datetime for MongoDB date comparisons
        last_30_days_dt = datetime.combine(last_30_days, datetime.min.time())

        try:
            col = get_mongo_collection('consumption_consumptiondata')
            user_id = user.id

            # Overall stats for current user
            stats_pipeline = [
                {'$match': {'user_id': user_id, 'date': {'$gte': last_30_days_dt}}},
                {'$group': {
                    '_id': None,
                    'total': {'$sum': '$consumption'},
                    'avg': {'$avg': '$consumption'},
                    'peak': {'$max': '$consumption'}
                }}
            ]
            stats_result = list(col.aggregate(stats_pipeline))
            stats = stats_result[0] if stats_result else {'total': 0, 'avg': 0, 'peak': 0}
            
            avg_val = stats.get('avg') or 0

            # --- GROUP BY queries — use raw pymongo to bypass djongo GROUP BY bug ---
            col = get_mongo_collection('consumption_consumptiondata')
            user_id = user.id

            # Device breakdown: group by device_name, sum consumption
            device_pipeline = [
                {'$match': {'user_id': user_id, 'date': {'$gte': last_30_days_dt}}},
                {'$group': {'_id': '$device_name', 'consumption': {'$sum': '$consumption'}}},
                {'$sort': {'consumption': -1}}
            ]
            device_breakdown = [
                {'deviceName': doc['_id'], 'consumption': round(doc['consumption'], 2)}
                for doc in col.aggregate(device_pipeline)
            ]

            # Daily usage: group by date, sum consumption
            daily_pipeline = [
                {'$match': {'user_id': user_id, 'date': {'$gte': last_30_days_dt}}},
                {'$group': {
                    '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$date'}},
                    'consumption': {'$sum': '$consumption'}
                }},
                {'$sort': {'_id': 1}}
            ]
            daily_usage = [
                {'date': doc['_id'], 'consumption': round(doc['consumption'], 2)}
                for doc in col.aggregate(daily_pipeline)
            ]

            return Response({
                'totalConsumption': round(stats.get('total') or 0, 2),
                'avgDailyConsumption': round(avg_val, 2),
                'peakConsumption': round(stats.get('peak') or 0, 2),
                'predictedNextMonth': round(avg_val * 30, 2),
                'deviceBreakdown': device_breakdown,
                'dailyData': daily_usage,
            })

        except Exception as e:
            import traceback
            print(f"DashboardStatsView ERROR: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=500)


class UserSummaryView(views.APIView):
    def get(self, request):
        user = request.user
        try:
            col = get_mongo_collection('consumption_consumptiondata')
            user_pipeline = [
                {'$match': {'user_id': user.id}},
                {'$group': {'_id': None, 'total': {'$sum': '$consumption'}}}
            ]
            user_result = list(col.aggregate(user_pipeline))
            total = user_result[0]['total'] if user_result else 0

            # device distinct count via raw pymongo (djongo DISTINCT may also fail)
            col = get_mongo_collection('consumption_consumptiondata')
            device_count = len(col.distinct('device_name', {'user_id': user.id}))

            return Response({
                "total_consumption": round(total, 2),
                "average_daily": round(total / 30, 2) if total > 0 else 0,
                "active_devices": device_count
            })
        except Exception as e:
            import traceback
            print(f"UserSummaryView ERROR: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=500)


class AdminSummaryView(views.APIView):
    def get(self, request):
        if request.user.role != 'admin':
            return Response({"error": "Unauthorized"}, status=403)

        try:
            col = get_mongo_collection('consumption_consumptiondata')
            admin_pipeline = [
                {'$group': {'_id': None, 'total': {'$sum': '$consumption'}}}
            ]
            admin_result = list(col.aggregate(admin_pipeline))
            total = admin_result[0]['total'] if admin_result else 0
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
            import traceback
            print(f"AdminSummaryView ERROR: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=500)


class PeakHoursView(views.APIView):
    def get(self, request):
        try:
            col = get_mongo_collection('consumption_consumptiondata')
            # Realistic residential load profile shape (24 hours)
            # Morning peak (7-9am) and evening peak (6-10pm)
            base_profile = [
                0.3, 0.2, 0.2, 0.2, 0.3, 0.5,  # 00-05
                0.8, 1.2, 1.5, 1.0, 0.7, 0.6,  # 06-11
                0.6, 0.7, 0.8, 1.0, 1.2, 1.8,  # 12-17
                2.5, 2.8, 2.2, 1.5, 0.8, 0.5   # 18-23
            ]

            # Scale by user's average daily consumption using raw pymongo
            peak_pipeline = [
                {'$match': {'user_id': request.user.id}},
                {'$group': {'_id': None, 'avg': {'$avg': '$consumption'}}}
            ]
            peak_result = list(col.aggregate(peak_pipeline))
            avg_daily = peak_result[0]['avg'] if peak_result else 10
            scale = avg_daily / sum(base_profile)

            hours = [f"{i:02d}:00" for i in range(24)]
            data = []
            for h, val in zip(hours, base_profile):
                noise = random.uniform(0.9, 1.1)
                data.append({"hour": h, "value": round(val * scale * noise, 2)})

            return Response(data)
        except Exception as e:
            import traceback
            print(f"PeakHoursView ERROR: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=500)


class MonthlyComparisonView(views.APIView):
    def get(self, request):
        data = []
        today = datetime.now().date()

        try:
            col = get_mongo_collection('consumption_consumptiondata')
            user_id = request.user.id

            for i in range(5, -1, -1):
                first_day = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
                last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)
                month_name = first_day.strftime('%b')

                first_dt = datetime.combine(first_day, datetime.min.time())
                last_dt = datetime.combine(last_day, datetime.max.time())

                # Current period sum via raw pymongo
                cur_pipeline = [
                    {'$match': {'user_id': user_id, 'date': {'$gte': first_dt, '$lte': last_dt}}},
                    {'$group': {'_id': None, 'total': {'$sum': '$consumption'}}}
                ]
                cur_result = list(col.aggregate(cur_pipeline))
                current_month_sum = cur_result[0]['total'] if cur_result else 0

                # Previous year comparison — guard against leap-year date errors
                try:
                    prev_first = first_day.replace(year=first_day.year - 1)
                    prev_last = last_day.replace(year=last_day.year - 1)
                    prev_first_dt = datetime.combine(prev_first, datetime.min.time())
                    prev_last_dt = datetime.combine(prev_last, datetime.max.time())

                    prev_pipeline = [
                        {'$match': {'user_id': user_id, 'date': {'$gte': prev_first_dt, '$lte': prev_last_dt}}},
                        {'$group': {'_id': None, 'total': {'$sum': '$consumption'}}}
                    ]
                    prev_result = list(col.aggregate(prev_pipeline))
                    previous_month_sum = prev_result[0]['total'] if prev_result else 0
                except (ValueError, OverflowError):
                    previous_month_sum = 0

                # Simulate a baseline if no previous data exists
                if previous_month_sum == 0 and current_month_sum > 0:
                    previous_month_sum = current_month_sum * random.uniform(0.8, 1.2)

                data.append({
                    "month": month_name,
                    "current": round(current_month_sum, 2),
                    "previous": round(previous_month_sum, 2)
                })

            return Response(data)
        except Exception as e:
            import traceback
            print(f"MonthlyComparisonView ERROR: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=500)
