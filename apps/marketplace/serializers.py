"""Serializers for Marketplace app."""
from rest_framework import serializers
from .models import Listing, Offer


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing with farmer name."""
    farmer_name = serializers.StringRelatedField(source='farmer')

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['created_at']


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer with buyer name."""
    buyer_name = serializers.StringRelatedField(source='buyer')

    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['created_at']
