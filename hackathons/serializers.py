from rest_framework import serializers
from rest_framework.reverse import reverse


# from api.serializers import UserPublicSerializer

from .models import Hackathon
from syntaq_auth.serializers import PublicUserDetailSerializer

from .validators import *


class HackathonSerializer(serializers.ModelSerializer):
    organizerId = serializers.PrimaryKeyRelatedField(read_only=True)
    organizer = PublicUserDetailSerializer(read_only=True, source="organizerId")
    start_date = serializers.DateTimeField()

    def validate(self, attrs):
        # print(attrs["title"])
        validate_dates(attrs)
        validate_team_size(attrs)

        return super().validate(attrs)

    class Meta:
        model = Hackathon
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "start_date",
            "end_date",
            "organizerId",
            "organizer",
            "registrationOpen",
            "registrationClose",
            "location",
            "created_at",
            "updated_at",
            "photo",
            "maxTeamSize",
            "minTeamSize",
        ]
