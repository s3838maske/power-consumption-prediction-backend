from django.urls import path
from .views import DeviceViewSet, DeviceDetailView

urlpatterns = [
    path('', DeviceViewSet.as_view()),
    path('<str:id>', DeviceDetailView.as_view()),
]
