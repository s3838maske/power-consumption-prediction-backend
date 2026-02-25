from django.urls import path
from .views import ReportViewSet, DailyReportView, WeeklyReportView, MonthlyReportView, DownloadExcelReportView, DownloadPdfReportView

urlpatterns = [
    path('', ReportViewSet.as_view(), name='reports-list'),
    path('daily', DailyReportView.as_view(), name='report-daily'),
    path('weekly', WeeklyReportView.as_view(), name='report-weekly'),
    path('monthly', MonthlyReportView.as_view(), name='report-monthly'),
    path('download-excel', DownloadExcelReportView.as_view(), name='report-download-excel'),
    path('download-pdf', DownloadPdfReportView.as_view(), name='report-download-pdf'),
]
