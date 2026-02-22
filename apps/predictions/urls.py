from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PredictionViewSet, GeneratePredictionView, PredictionHistoryView, CompareActualView, PredictionByDeviceView

router = SimpleRouter(trailing_slash=False)
router.register(r'data', PredictionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate', GeneratePredictionView.as_view(), name='prediction-generate'),
    path('history', PredictionHistoryView.as_view(), name='prediction-history'),
    path('compare-actual', CompareActualView.as_view(), name='compare-actual'),
    path('<int:device_id>', PredictionByDeviceView.as_view(), name='prediction-by-device'),
]
