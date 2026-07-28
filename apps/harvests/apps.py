"""App configuration for harvests app."""
from django.apps import AppConfig


class HarvestsConfig(AppConfig):
    """Configuration for the Harvests app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.harvests'