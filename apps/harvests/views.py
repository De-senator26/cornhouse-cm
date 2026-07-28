"""API views for Harvests app."""
from rest_framework import viewsets, permissions
from .models import StorageMethod, Harvest, Loss
from .serializers import StorageMethodSerializer, HarvestSerializer, LossSerializer


class StorageMethodViewSet(viewsets.ModelViewSet):
    """ViewSet for StorageMethod."""
    queryset = StorageMethod.objects.all()  # pylint: disable=no-member
    serializer_class = StorageMethodSerializer
    permission_classes = [permissions.IsAuthenticated]


class HarvestViewSet(viewsets.ModelViewSet):
    """ViewSet for Harvest."""
    queryset = Harvest.objects.all()  # pylint: disable=no-member
    serializer_class = HarvestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['farmer', 'storage_method', 'is_sold']
    search_fields = ['quality_grade']


class LossViewSet(viewsets.ModelViewSet):
    """ViewSet for Loss."""
    queryset = Loss.objects.all()  # pylint: disable=no-member
    serializer_class = LossSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['harvest', 'loss_type']
    