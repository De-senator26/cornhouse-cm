"""URLs for Marketplace app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, OfferViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'offers', OfferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]