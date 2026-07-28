"""App configuration for finance app."""
from django.apps import AppConfig


class FinanceConfig(AppConfig):
    """Configuration for the Finance app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.finance'
    