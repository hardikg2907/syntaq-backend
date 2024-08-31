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
from .serializers import TeamSerializer, InvitationSerializer, TeamMemberSerializer
from .tasks import send_invitation_email


class CreateTeamView(generics.CreateAPIView):
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        hackathon = get_object_or_404(
            Hackathon, id=self.request.data.get("hackathon_id")
        )
        user = get_user(self.request.data.get("user_email"))
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
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class SendInvitationView(generics.CreateAPIView):
    serializer_class = InvitationSerializer

    def create(self, request, *args, **kwargs):
        # print(request.user)
        team = get_object_or_404(Team, id=self.kwargs["team_id"])
        invitation_data = {
            "team": team.pk,
            "receiver_email": request.data.get("receiver_email"),
        }
        serializer = self.get_serializer(data=invitation_data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.perform_create(serializer)
            invitation = serializer.save()
            transaction.on_commit(lambda: send_invitation_email.delay(invitation, team))
            # send_invitation_email.delay(invitation, team)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AcceptInvitationView(generics.UpdateAPIView):
    serializer_class = InvitationSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        invitation = get_object_or_404(
            Invitation,
            id=self.kwargs["invitation_id"],
            receiver_email=request.data.get("user_email"),
        )
        invitation.accepted = True
        user = get_user(request.data.get("user_email"))
        with transaction.atomic():
            invitation.save()
            TeamMember.objects.create(
                team=invitation.team, user=user, is_confirmed=True
            )
        return Response(
            {"detail": "You have joined the team."}, status=status.HTTP_200_OK
        )


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
