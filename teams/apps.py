from django.apps import AppConfig
import posthog
import os


class TeamsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "teams"

    def ready(self):
        posthog.api_key = os.getenv("POSTHOG_API_KEY")
        posthog.host = os.getenv("POSTHOG_HOST")
