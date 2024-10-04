from django.apps import AppConfig
import posthog


class TeamsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "teams"

    def ready(self):
        posthog.api_key = "phc_hegIFzYoiooISUbdtkhiT3JDG4itI3DglJGw4vLVv0W"
        posthog.host = "https://us.i.posthog.com"
