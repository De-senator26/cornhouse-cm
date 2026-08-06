"""
URL configuration for cornhouse project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.analytics.views import dashboard_stats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.web.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('apps.users.urls')),
    path('api/harvests/', include('apps.harvests.urls')),
    path('api/marketplace/', include('apps.marketplace.urls')),
    path('api/finance/', include('apps.finance.urls')),
    path('api/knowledge/', include('apps.knowledge.urls')),
    path('api/analytics/stats/', dashboard_stats, name='api_analytics_stats'),
    path('analytics/', include('apps.analytics.urls')),
    path('chat/', include('apps.chatbot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


