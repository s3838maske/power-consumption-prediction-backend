from django.urls import path
from .views import GeneratePredictionView, PredictionHistoryView, CompareActualView, PredictionByDeviceView

urlpatterns = [
    path('generate', GeneratePredictionView.as_view(), name='prediction-generate'),
    path('history', PredictionHistoryView.as_view(), name='prediction-history'),
    path('compare-actual', CompareActualView.as_view(), name='compare-actual'),
    path('<str:device_id>', PredictionByDeviceView.as_view(), name='prediction-by-device'),
]
