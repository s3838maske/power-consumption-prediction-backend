"""
URL configuration for power consumption prediction project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/devices/', include('apps.devices.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/consumption/', include('apps.consumption.urls')),
    path('api/prediction/', include('apps.predictions.urls')),
    path('api/alerts/', include('apps.alerts.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/dashboard/', include('apps.consumption.urls')), # Dashboard info usually comes from consumption data
    path('api/admin/', include('apps.admin_panel.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
