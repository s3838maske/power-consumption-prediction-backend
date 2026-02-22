from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
