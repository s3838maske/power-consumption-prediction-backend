from django.urls import path
from .views import AlertViewSet, SetThresholdView, UpdateAlertView

urlpatterns = [
    path('', AlertViewSet.as_view(), name='alerts-list'),
    path('set-threshold', SetThresholdView.as_view(), name='alert-set-threshold'),
    path('update', UpdateAlertView.as_view(), name='alert-update'),
    path('<str:id>', AlertViewSet.as_view(), name='alert-detail'),
]
