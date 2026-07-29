from django.urls import path
from .views import dashboard_stats, dashboard_page

urlpatterns = [
    path('', dashboard_page, name='analytics_dashboard'),
    path('stats/', dashboard_stats, name='analytics_stats'),
]
