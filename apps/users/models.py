"""Custom User model for CornHouse."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extends Django's AbstractUser with CornHouse-specific fields:
    - phone (unique, required)
    - role (farmer, buyer, partner, admin)
    - is_verified (boolean)
    """
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
        ('partner', 'Partner'),
        ('admin', 'Admin'),
    )
    phone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='farmer')
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.username)
