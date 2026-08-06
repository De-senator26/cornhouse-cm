"""App configuration for web app."""
from django.apps import AppConfig


class WebConfig(AppConfig):
    """Configuration for the Web app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.web'