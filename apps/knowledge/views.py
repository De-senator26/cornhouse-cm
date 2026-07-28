"""API views for Knowledge app."""
from rest_framework import viewsets, permissions
from .models import Category, Tag, Article
from .serializers import CategorySerializer, TagSerializer, ArticleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet for Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    """ViewSet for Article."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['title', 'content']