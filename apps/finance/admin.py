"""Admin registration for finance models."""
from django.contrib import admin
from .models import Grant, Loan, Repayment


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    """Admin for Grant applications."""
    list_display = ('farmer', 'amount_requested', 'status', 'application_date', 'decision_date')
    list_filter = ('status', 'application_date', 'farmer')
    search_fields = ('farmer__username', 'farmer__phone', 'purpose')
    readonly_fields = ('application_date',)
    fieldsets = (
        ('Applicant', {'fields': ('farmer',)}),
        ('Grant Details', {'fields': ('amount_requested', 'purpose')}),
        ('Review', {'fields': ('status', 'reviewed_by', 'decision_date', 'notes')}),
    )


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Admin for Loan applications."""
    list_display = ('farmer', 'amount', 'interest_rate', 'duration_months', 'status', 'application_date')
    list_filter = ('status', 'application_date', 'farmer')
    search_fields = ('farmer__username', 'farmer__phone', 'purpose')
    readonly_fields = ('application_date',)
    fieldsets = (
        ('Applicant', {'fields': ('farmer',)}),
        ('Loan Details', {'fields': ('amount', 'interest_rate', 'duration_months', 'purpose')}),
        ('Review', {'fields': ('status', 'approved_by', 'disbursement_date', 'repayment_due', 'notes')}),
    )


@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    """Admin for Loan Repayments."""
    list_display = ('loan', 'amount_paid', 'payment_date', 'payment_method')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('loan__farmer__username', 'notes')
    