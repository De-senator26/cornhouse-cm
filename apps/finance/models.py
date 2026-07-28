"""Finance models for CornHouse."""
from django.db import models
from django.conf import settings


class Grant(models.Model):
    """Grant applications from farmers."""
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
    )
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='grant_applications',
        limit_choices_to={'role': 'farmer'}
    )
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.TextField(help_text="What will the grant be used for?")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grants_reviewed',
        limit_choices_to={'role__in': ['admin', 'partner']}
    )
    application_date = models.DateField(auto_now_add=True)
    decision_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Admin notes or feedback")

    def __str__(self) -> str:
        return f"{self.farmer.get_username()} - {self.amount_requested} XAF - {self.status}"  # pylint: disable=no-member


class Loan(models.Model):
    """Loan applications from farmers."""
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('repaid', 'Repaid'),
        ('defaulted', 'Defaulted'),
    )
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loan_applications',
        limit_choices_to={'role': 'farmer'}
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual interest rate %")
    duration_months = models.PositiveIntegerField()
    purpose = models.TextField(help_text="What will the loan be used for?")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='loans_approved',
        limit_choices_to={'role__in': ['admin', 'partner']}
    )
    application_date = models.DateField(auto_now_add=True)
    disbursement_date = models.DateField(null=True, blank=True)
    repayment_due = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.farmer.get_username()} - {self.amount} XAF - {self.status}"  # pylint: disable=no-member


class Repayment(models.Model):
    """Repayment records for loans."""
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name='repayments'
    )
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=50,
        choices=(
            ('cash', 'Cash'),
            ('bank_transfer', 'Bank Transfer'),
            ('mobile_money', 'Mobile Money'),
            ('other', 'Other'),
        ),
        default='mobile_money'
    )
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.loan} - {self.amount_paid} XAF - {self.payment_date}"
    