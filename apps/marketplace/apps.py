"""App configuration for marketplace app."""
from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    """Configuration for the Marketplace app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.marketplace'