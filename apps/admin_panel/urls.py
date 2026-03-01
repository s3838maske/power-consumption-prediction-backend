from django.urls import path
from .views import (
    AdminUserListView, UserActivateView, AdminProductView
)

urlpatterns = [
    path('users', AdminUserListView.as_view(), name='admin-users'),
    path('users/<int:id>/activate', UserActivateView.as_view(), name='admin-user-activate'),
    path('product', AdminProductView.as_view(), name='admin-product'),
]
