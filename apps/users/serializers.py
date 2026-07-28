"""Serializers for Users app."""
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'is_verified']
        read_only_fields = ['id', 'is_verified']
        