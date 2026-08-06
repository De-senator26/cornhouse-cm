"""App configuration for analytics app."""
from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    """Configuration for the Analytics app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.analytics'
