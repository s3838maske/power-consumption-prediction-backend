from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import AlertViewSet, SetThresholdView, UpdateAlertView

router = SimpleRouter(trailing_slash=False)
router.register(r'', AlertViewSet)

urlpatterns = [
    path('set-threshold', SetThresholdView.as_view(), name='alert-set-threshold'),
    path('update', UpdateAlertView.as_view(), name='alert-update'),
    path('<int:id>', AlertViewSet.as_view({'delete': 'destroy'}), name='alert-delete'),
    path('', include(router.urls)),
]
