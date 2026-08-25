"""Custom authentication backend for CornHouse allowing login by Username, Email, or Phone."""
import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

logger = logging.getLogger(__name__)
User = get_user_model()


class EmailOrPhoneOrUsernameBackend(ModelBackend):
    """
    Allows authentication via username, email (case-insensitive), or phone number.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email') or kwargs.get('phone')

        if not username or not password:
            return None

        # Clean string inputs
        identifier = str(username).strip()

        try:
            # Match by username, email, or phone
            user = User.objects.filter(
                Q(username__iexact=identifier) |
                Q(email__iexact=identifier) |
                Q(phone__iexact=identifier)
            ).first()

            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception as exc:
            logger.error("Authentication backend error for '%s': %s", identifier, exc)
            return None

        return None
