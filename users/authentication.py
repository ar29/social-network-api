# users/authentication.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email')
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return None
        if self.user_can_authenticate(user):
            return user
        raise Exception(self.user_can_authenticate(user))
        return None
