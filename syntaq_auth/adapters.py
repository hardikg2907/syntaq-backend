from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from syntaq_auth.models import CustomUserModel


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):

    def populate_user(self, request, sociallogin, data):
        # print(data)
        # print(sociallogin)

        user = sociallogin.user
        user.email = data.get("email")
        user.username = (
            data.get("name").replace(" ", "").lower()
        )  # Example of generating a username
        user.firstName = data.get("given_name")
        user.lastName = data.get("family_name")
        return user
