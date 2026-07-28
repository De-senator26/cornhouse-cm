"""Serializers for Knowledge app."""
from rest_framework import serializers
from .models import Category, Tag, Article


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category."""
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag."""
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for Article with related names."""
    category_name = serializers.StringRelatedField(source='category')
    tags_names = serializers.StringRelatedField(many=True, source='tags')

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['published_at', 'updated_at']
        