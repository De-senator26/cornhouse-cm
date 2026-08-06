"""Models for web frontend, including user feedback and reviews."""
from django.db import models
from django.conf import settings


class UserFeedback(models.Model):
    """User reviews and feedback for CornHouse."""
    CATEGORY_CHOICES = (
        ('general', 'General Experience'),
        ('post_harvest', 'Post-Harvest Management'),
        ('marketplace', 'Marketplace & Trade'),
        ('finance', 'Grants & Financial Inclusion'),
        ('chatbot', 'AI Agribot Assistant'),
        ('usability', 'App Usability & Performance'),
    )

    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
        ('partner', 'Partner / Investor'),
        ('other', 'Community Member'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedbacks'
    )
    name = models.CharField(max_length=100, blank=True, help_text="User's display name")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')
    rating = models.PositiveSmallIntegerField(default=5, help_text="Rating between 1 and 5 stars")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    comment = models.TextField(help_text="User feedback comments and suggestions")
    is_public = models.BooleanField(default=True, help_text="Show in public testimonials on home page")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Feedback"
        verbose_name_plural = "User Feedbacks"

    def __str__(self) -> str:
        display_name = self.name or (self.user.username if self.user else "Anonymous")
        return f"{display_name} ({self.rating}★) - {self.get_category_display()}"
