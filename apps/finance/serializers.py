"""Serializers for Finance app."""
from rest_framework import serializers
from .models import Grant, Loan, Repayment


class GrantSerializer(serializers.ModelSerializer):
    """Serializer for Grant with farmer name."""
    farmer_name = serializers.StringRelatedField(source='farmer')

    class Meta:
        model = Grant
        fields = '__all__'
        read_only_fields = ['application_date']


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for Loan with farmer name."""
    farmer_name = serializers.StringRelatedField(source='farmer')

    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['application_date']


class RepaymentSerializer(serializers.ModelSerializer):
    """Serializer for Repayment."""
    class Meta:
        model = Repayment
        fields = '__all__'
        read_only_fields = ['payment_date']
        