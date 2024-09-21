# teams/serializers.py

from rest_framework import serializers
from .models import Team, Invitation, TeamMember
from hackathons.models import Hackathon
from syntaq_auth.models import CustomUserModel


class UserTeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ["email", "first_name", "last_name"]


class TeamMemberSerializer(serializers.ModelSerializer):
    userFields = UserTeamMemberSerializer(read_only=True, source="user")

    class Meta:
        model = TeamMember
        fields = ["id", "is_confirmed", "userFields"]


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        read_only_fields = ["created_at", "id"]
        model = Team
        fields = [
            "id",
            "hackathon",
            "name",
            "leader",
            "created_at",
            "registration_complete",
        ]


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ["id", "sent_at"]
        model = Invitation
        fields = ["id", "team", "receiver_email", "sent_at", "accepted"]


class TeamTeamMemberSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(read_only=True, many=True)

    class Meta:
        model = Team
        fields = ["id", "name", "members", "leader", "hackathon"]


class InvitationTeamMemberSerializer(serializers.ModelSerializer):
    team = TeamTeamMemberSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ["id", "team", "receiver_email", "sent_at", "accepted"]
