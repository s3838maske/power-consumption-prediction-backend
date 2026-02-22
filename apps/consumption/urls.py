from django.urls import path
from .views import UploadConsumptionView, ConsumptionHistoryView, ConsumptionDetailView
from .stats_views import DashboardStatsView, UserSummaryView, AdminSummaryView, PeakHoursView, MonthlyComparisonView
from .prediction_views import PredictionView

urlpatterns = [
    # Consumption endpoints
    path('upload-excel', UploadConsumptionView.as_view(), name='upload-excel'),
    path('history', ConsumptionHistoryView.as_view(), name='consumption-history'),
    path('<int:id>', ConsumptionDetailView.as_view(), name='consumption-detail'),
    
    # Dashboard endpoints (via /api/dashboard/ in config/urls.py)
    path('user-summary', UserSummaryView.as_view(), name='user-summary'),
    path('admin-summary', AdminSummaryView.as_view(), name='admin-summary'),
    path('peak-hours', PeakHoursView.as_view(), name='peak-hours'),
    path('monthly-comparison', MonthlyComparisonView.as_view(), name='monthly-comparison'),
    
    # Other stats
    path('dashboard-stats', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('predictions', PredictionView.as_view(), name='predictions'),
]
