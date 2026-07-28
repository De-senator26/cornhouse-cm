"""Harvest models for CornHouse."""
from django.db import models
from django.conf import settings


class StorageMethod(models.Model):
    """Predefined storage options (e.g., hermetic bag, silo, open)."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:  # pylint: disable=invalid-str-returned
        return self.name


class Harvest(models.Model):
    """A maize harvest recorded by a farmer."""
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='harvests'
    )
    crop_type = models.CharField(max_length=20, default='maize')
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    harvest_date = models.DateField()
    storage_method = models.ForeignKey(
        StorageMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    moisture_content = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Percentage"
    )
    quality_grade = models.CharField(
        max_length=20,
        blank=True,
        help_text="e.g., A, B, C"
    )
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.farmer.get_username()} - {self.harvest_date} - {self.quantity_kg}kg"  # pylint: disable=no-member


class Loss(models.Model):
    """Record of post-harvest losses."""
    LOSS_TYPES = (
        ('spoilage', 'Spoilage'),
        ('insect', 'Insect Damage'),
        ('rodent', 'Rodent Damage'),
        ('theft', 'Theft'),
        ('other', 'Other'),
    )
    harvest = models.ForeignKey(
        Harvest,
        on_delete=models.CASCADE,
        related_name='losses'
    )
    loss_type = models.CharField(max_length=20, choices=LOSS_TYPES)
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    reported_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.loss_type} - {self.quantity_kg}kg"
    