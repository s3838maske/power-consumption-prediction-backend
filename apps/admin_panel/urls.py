from django.urls import path
from .views import (
    AdminUserListView, UserActivateView, AdminLogsView, 
    AdminCategoryView, AdminCategoryDetailView, AdminProductView
)

urlpatterns = [
    path('users', AdminUserListView.as_view(), name='admin-users'),
    path('users/<int:id>/activate', UserActivateView.as_view(), name='admin-user-activate'),
    path('logs', AdminLogsView.as_view(), name='admin-logs'),
    path('category', AdminCategoryView.as_view(), name='admin-category'),
    path('category/<int:id>', AdminCategoryDetailView.as_view(), name='admin-category-detail'),
    path('product', AdminProductView.as_view(), name='admin-product'),
]
