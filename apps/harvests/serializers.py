"""Serializers for Harvests app."""
from rest_framework import serializers
from .models import StorageMethod, Harvest, Loss


class StorageMethodSerializer(serializers.ModelSerializer):
    """Serializer for StorageMethod."""
    class Meta:
        model = StorageMethod
        fields = '__all__'


class HarvestSerializer(serializers.ModelSerializer):
    """Serializer for Harvest with farmer name."""
    farmer_name = serializers.StringRelatedField(source='farmer', read_only=True)

    class Meta:
        model = Harvest
        fields = '__all__'
        read_only_fields = ['created_at']


class LossSerializer(serializers.ModelSerializer):
    """Serializer for Loss."""
    class Meta:
        model = Loss
        fields = '__all__'
        read_only_fields = ['reported_date']
        