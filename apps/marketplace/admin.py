"""Admin registration for marketplace models."""
from django.contrib import admin
from django.utils.html import format_html
from .models import Listing, Offer


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'quantity_kg', 'price_per_kg', 'available_until', 'is_active', 'image_preview')
    list_filter = ('is_active', 'available_until', 'farmer')
    search_fields = ('farmer__username', 'quality_description')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Image'


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('listing', 'buyer', 'offered_price', 'quantity_kg', 'status')
    list_filter = ('status', 'buyer')
    search_fields = ('buyer__username', 'listing__farmer__username')
