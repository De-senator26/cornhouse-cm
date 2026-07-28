"""Admin registration for knowledge models."""
from django.contrib import admin
from .models import Category, Tag, Article   # correct relative import


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category."""
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for Tag."""
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin for Article."""
    list_display = ('title', 'category', 'is_featured', 'published_at')
    list_filter = ('category', 'is_featured', 'published_at')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {'fields': ('title', 'content', 'category', 'tags')}),
        ('Metadata', {'fields': ('author', 'is_featured')}),
    )
    