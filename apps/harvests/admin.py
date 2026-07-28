"""Admin registration for harvest models."""
from django.contrib import admin
from .models import StorageMethod, Harvest, Loss


@admin.register(StorageMethod)
class StorageMethodAdmin(admin.ModelAdmin):
    """Admin for StorageMethod."""
    list_display = ('name', 'description')


@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    """Admin for Harvest."""
    list_display = ('farmer', 'harvest_date', 'quantity_kg', 'storage_method', 'is_sold')
    list_filter = ('farmer', 'harvest_date', 'storage_method', 'is_sold')
    search_fields = ('farmer__username', 'farmer__phone', 'quality_grade')


@admin.register(Loss)
class LossAdmin(admin.ModelAdmin):
    """Admin for Loss."""
    list_display = ('harvest', 'loss_type', 'quantity_kg', 'reported_date')
    list_filter = ('loss_type', 'reported_date')
    search_fields = ('harvest__farmer__username',)
    