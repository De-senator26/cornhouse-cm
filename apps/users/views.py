"""API views for Users app."""
from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User."""
    queryset = User.objects.all()  # pylint: disable=no-member
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['role', 'is_verified']
    search_fields = ['username', 'email', 'phone']
    