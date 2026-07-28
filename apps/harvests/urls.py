"""URLs for Harvests app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import StorageMethodViewSet, HarvestViewSet, LossViewSet

router = DefaultRouter()
router.register(r'storage-methods', StorageMethodViewSet)
router.register(r'harvests', HarvestViewSet)
router.register(r'losses', LossViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
