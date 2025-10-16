from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authenticate using either email or username in the "username" field.
    Keeps Django's default permission behavior via ModelBackend inheritance.
    """

    def authenticate(self, request, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        if username is None:
            # Some callers might pass email through kwargs
            username = kwargs.get("email")

        if not username or not password:
            return None

        UserModel = get_user_model()

        try:
            user = (
                UserModel.objects.filter(
                    Q(email__iexact=username) | Q(username__iexact=username)
                )
                .order_by("id")
                .first()
            )
        except Exception:
            return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id: int):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


