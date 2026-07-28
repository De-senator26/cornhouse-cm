"""API views for Marketplace app."""
from rest_framework import viewsets, permissions
from .models import Listing, Offer
from .serializers import ListingSerializer, OfferSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for Listing."""
    queryset = Listing.objects.all()  # pylint: disable=no-member
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['farmer', 'is_active']
    search_fields = ['quality_description']


class OfferViewSet(viewsets.ModelViewSet):
    """ViewSet for Offer."""
    queryset = Offer.objects.all()  # pylint: disable=no-member
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['listing', 'buyer', 'status']
    