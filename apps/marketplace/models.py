"""Marketplace models for CornHouse."""
from django.db import models
from django.conf import settings
from apps.harvests.models import Harvest


class Listing(models.Model):
    """A produce listing (maize) created by a farmer."""
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings',
        limit_choices_to={'role': 'farmer'}
    )
    harvest = models.ForeignKey(
        Harvest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='listings',
        help_text="Optional: link to a specific harvest"
    )
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    quality_description = models.TextField(blank=True, help_text="e.g., grade A, moisture content")
    available_until = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='listings/', null=True, blank=True, help_text="Upload a photo of your maize")

    def __str__(self) -> str:
        return f"{self.farmer.get_username()} - {self.quantity_kg}kg at {self.price_per_kg} XAF/kg"  # pylint: disable=no-member


class Offer(models.Model):
    """An offer made by a buyer on a listing."""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('countered', 'Countered'),
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='offers'
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='offers',
        limit_choices_to={'role': 'buyer'}
    )
    offered_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.buyer.get_username()} - {self.listing} - {self.offered_price} XAF/kg"  # pylint: disable=no-member