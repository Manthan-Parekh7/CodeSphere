from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as DjangoAdminUser

User = get_user_model()


class EmailAuthBackend(ModelBackend):
    """
    Authenticate HomePageAuth users (Students & Teachers) using email instead of username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # ✅ Check if email exists in HomePageAuth.User
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None  # If authentication fails, return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class AdminAuthBackend(ModelBackend):
    """
    Authenticate Django Admin superusers using default Django auth.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # ✅ Check if username belongs to a Django Admin superuser
            admin_user = DjangoAdminUser.objects.get(
                username=username, is_superuser=True)
            if admin_user.check_password(password):
                return admin_user
        except DjangoAdminUser.DoesNotExist:
            return None
        return None  # If authentication fails, return None

    def get_user(self, user_id):
        try:
            return DjangoAdminUser.objects.get(pk=user_id)
        except DjangoAdminUser.DoesNotExist:
            return None
