"""Knowledge models for CornHouse."""
from django.db import models
from django.conf import settings


class Category(models.Model):
    """Category for articles (e.g., Climate, Storage, Finance)."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:  # pylint: disable=invalid-str-returned
        return self.name


class Tag(models.Model):
    """Optional tags for extra filtering (e.g., drought, irrigation)."""
    name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:  # pylint: disable=invalid-str-returned
        return self.name


class Article(models.Model):
    """Knowledge article for farmers and partners."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_articles',
        help_text="Optional – can be an admin or expert"
    )
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self) -> str:  # pylint: disable=invalid-str-returned
        return self.title
