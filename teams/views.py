from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from os import getenv

from hackathons.models import Hackathon
from syntaq_auth.models import CustomUserModel
from syntaq_auth.views import get_user
from .models import Team, Invitation, TeamMember
from .serializers import (
    TeamSerializer,
    InvitationSerializer,
    TeamMemberSerializer,
    InvitationTeamMemberSerializer,
)
from .tasks import send_invitation_email

import posthog

# Team Views


class CreateTeamView(generics.CreateAPIView):
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        try:
            hackathon = get_object_or_404(
                Hackathon, id=self.request.data.get("hackathon_id")
            )
            # user = get_user(self.request.data.get("user_email"))
            user = request.user
            with transaction.atomic():
                serializer = self.get_serializer(
                    data={
                        "name": request.data.get("name"),
                        "hackathon": hackathon.pk,
                        "leader": user.pk,
                    }
                )
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                team = serializer.save()
                TeamMember.objects.create(team=team, user=user, is_confirmed=True)
            posthog.capture(
                user.pk,
                event="team_registration",
                properties={
                    "id": hackathon.pk,
                },
            )
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateTeamAPIView(generics.UpdateAPIView):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        team = self.get_object()
        if team.leader != request.user:
            return Response(
                {"error": "You are not the leader of this team."},
                status=status.HTTP_403_FORBIDDEN,
            )
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)


class TeamDetailAPIView(generics.RetrieveAPIView):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    lookup_field = "pk"


class UserTeamInHackathonView(generics.RetrieveAPIView):
    serializer_class = TeamSerializer

    def get(self, request, *args, **kwargs):
        try:
            hackathon_id = kwargs.get("hackathon_id")
            user = request.user
            team_member = TeamMember.objects.filter(
                user=user, team__hackathon=hackathon_id
            ).first()
            if team_member:
                team = team_member.team
                return Response(TeamSerializer(team).data, status=status.HTTP_200_OK)
            return Response(None, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Team Members Views


class TeamMembersListAPIView(generics.ListAPIView):
    serializer_class = TeamMemberSerializer

    def get_queryset(self):
        team = self.get_object(Team, id=self.kwargs["team_id"])
        return team.members.all()


class TeamMembersAndInvitationsListView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        team = get_object_or_404(Team, id=self.kwargs["team_id"])
        members = team.members.all()
        invitations = team.invitations.all()
        members_serializer = TeamMemberSerializer(members, many=True)
        invitations_serializer = InvitationSerializer(invitations, many=True)
        return Response(
            {
                "accepted": members_serializer.data,
                "pending": invitations_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class TeamMembersDeleteAPIView(generics.DestroyAPIView):
    serializer_class = TeamMemberSerializer
    queryset = TeamMember.objects.all()
    lookup_field = "pk"

    def delete(self, request, *args, **kwargs):
        team_member = self.get_object()
        if team_member.team.leader != request.user:
            return Response(
                {"error": "You are not the leader of this team."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().delete(request, *args, **kwargs)


# Invitations Views


class TeamByInvitationView(generics.RetrieveAPIView):
    serializer_class = TeamSerializer

    def get_object(self):
        invitation = get_object_or_404(Invitation, id=self.kwargs["invitation_id"])
        return invitation.team


class InvitationsListView(generics.ListAPIView):
    serializer_class = InvitationSerializer

    def get_queryset(self):
        team = get_object_or_404(Team, id=self.kwargs["team_id"])
        return team.invitations.all()


class InvitationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = InvitationTeamMemberSerializer
    queryset = Invitation.objects.all()
    lookup_field = "pk"


class SendInvitationView(generics.CreateAPIView):
    serializer_class = InvitationSerializer

    def create(self, request, *args, **kwargs):
        # print(request.user)
        team = get_object_or_404(Team, id=self.kwargs["team_id"], leader=request.user)
        num_members = team.members.count()
        num_invitations = team.invitations.count()
        if num_members + num_invitations >= team.hackathon.maxTeamSize:
            return Response(
                {"error": "The team is already full."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        invitation_data = {
            "team": team.pk,
            "receiver_email": request.data.get("receiver_email"),
        }
        serializer = self.get_serializer(data=invitation_data)
        serializer.is_valid(raise_exception=True)
        receiver_email = request.data.get("receiver_email")
        if TeamMember.objects.filter(
            user__email=receiver_email, team__hackathon=team.hackathon
        ).exists():
            return Response(
                {"error": "The user is already part of a team in this hackathon."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        with transaction.atomic():
            self.perform_create(serializer)
            invitation = serializer.save()
            transaction.on_commit(lambda: send_invitation_email.delay(invitation, team))
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AcceptInvitationView(generics.UpdateAPIView):
    serializer_class = InvitationSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            invitation = get_object_or_404(
                Invitation,
                id=self.kwargs["invitation_id"],
                receiver_email=request.user.email,
            )
            user = request.user
            with transaction.atomic():
                TeamMember.objects.create(
                    team=invitation.team, user=user, is_confirmed=True
                )
                invitation.delete()
                team = invitation.team
                if team.is_valid():
                    team.register_team()
            return Response(
                {"detail": "You have joined the team."}, status=status.HTTP_200_OK
            )

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class InvitationDeleteAPIView(generics.DestroyAPIView):
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()
    lookup_field = "pk"

    def delete(self, request, *args, **kwargs):
        invitation = self.get_object()
        if invitation.team.leader != request.user:
            return Response(
                {"error": "You are not the leader of this team."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().delete(request, *args, **kwargs)


class RegisterTeamView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        leader = get_user(request.data.get("user_email"))
        team = get_object_or_404(Team, id=self.kwargs["team_id"], leader=leader)

        try:
            team.register_team()
            return Response(
                {"detail": "Team successfully registered for the hackathon!"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # return Response(
        #     {"detail": "All team members must confirm their participation."},
        #     status=status.HTTP_400_BAD_REQUEST,
        # )
