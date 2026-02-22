from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ReportViewSet, DailyReportView, WeeklyReportView, MonthlyReportView, DownloadExcelReportView, DownloadPdfReportView

router = SimpleRouter(trailing_slash=False)
router.register(r'data', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('daily', DailyReportView.as_view(), name='report-daily'),
    path('weekly', WeeklyReportView.as_view(), name='report-weekly'),
    path('monthly', MonthlyReportView.as_view(), name='report-monthly'),
    path('download-excel', DownloadExcelReportView.as_view(), name='report-download-excel'),
    path('download-pdf', DownloadPdfReportView.as_view(), name='report-download-pdf'),
]
