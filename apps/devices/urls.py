from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import DeviceViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'', DeviceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
