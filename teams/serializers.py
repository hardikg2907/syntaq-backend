# teams/serializers.py

from rest_framework import serializers
from .models import Team, Invitation, TeamMember
from hackathons.models import Hackathon
from syntaq_auth.models import CustomUserModel


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ["id", "team", "user", "joined_at", "is_confirmed"]


class TeamSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True, read_only=True)

    class Meta:
        read_only_fields = ["created_at", "id"]
        model = Team
        fields = ["id", "hackathon", "name", "leader", "created_at", "members"]


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["id", "team", "receiver_email", "sent_at", "accepted"]
