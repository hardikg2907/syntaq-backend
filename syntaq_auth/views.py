from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from os import getenv
from django.contrib.auth import get_user_model

from .models import CustomUserModel
from .adapters import CustomGoogleOAuth2Adapter


def get_user(email):
    try:
        user = CustomUserModel.objects.get(email=email)
        # print(user.userId)
        return user
    except CustomUserModel.DoesNotExist:
        # print("User with this email does not exist.")
        raise ValueError("User does not exist.")
        return None


class GoogleLoginView(SocialLoginView):
    authentication_classes = (
        []
    )  # Disable authentication, make sure to enable it in production
    adapter_class = GoogleOAuth2Adapter
    callback_url = (
        getenv("FRONTEND_URL") or "http://localhost:3000"
    )  # Your frontend URL
    client_class = OAuth2Client

    # def process_login(self):
    #     print(self.request.data)
    #     super().get_adapter(self.request).login(self.request, self.user)
