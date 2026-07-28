"""API views for Finance app."""
from rest_framework import viewsets, permissions
from .models import Grant, Loan, Repayment
from .serializers import GrantSerializer, LoanSerializer, RepaymentSerializer


class GrantViewSet(viewsets.ModelViewSet):
    """ViewSet for Grant."""
    queryset = Grant.objects.all()  # pylint: disable=no-member
    serializer_class = GrantSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['farmer', 'status']


class LoanViewSet(viewsets.ModelViewSet):
    """ViewSet for Loan."""
    queryset = Loan.objects.all()  # pylint: disable=no-member
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['farmer', 'status']


class RepaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Repayment."""
    queryset = Repayment.objects.all()  # pylint: disable=no-member
    serializer_class = RepaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['loan']
    