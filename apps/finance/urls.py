"""URLs for Finance app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import GrantViewSet, LoanViewSet, RepaymentViewSet

router = DefaultRouter()
router.register(r'grants', GrantViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'repayments', RepaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
