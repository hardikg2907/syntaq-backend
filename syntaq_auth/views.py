from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from os import getenv

class GoogleLoginView(SocialLoginView):
    authentication_classes = [] # Disable authentication, make sure to enable it in production
    adapter_class = GoogleOAuth2Adapter
    callback_url = getenv("FRONTEND_URL") or "http://localhost:3000" # Your frontend URL
    client_class = OAuth2Client