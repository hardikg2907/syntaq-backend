from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from os import getenv

from hackathons.models import Hackathon
from syntaq_auth.models import CustomUserModel
from syntaq_auth.views import get_user
from .models import Team, Invitation, TeamMember
from .serializers import TeamSerializer, InvitationSerializer, TeamMemberSerializer


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
            self.send_invitation_email(invitation, team)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def send_invitation_email(self, invitation, team):
        frontend_base_url = getenv("FRONTEND_URL")

        # Construct the frontend URL with team_id and invitation_id as query parameters
        accept_url = f"{frontend_base_url}/accept-invitation?teamId={team.id}&invitationId={invitation.id}"

        subject = f"Invitation to join team {team.name} for {team.hackathon.title}"

        leader_full_name = f"{team.leader.first_name} {team.leader.last_name}"

        message = render_to_string(
            "teams/invitation_email.html",
            {
                "team": team,
                "invitation": invitation,
                "accept_url": accept_url,
                "leader_full_name": leader_full_name,
            },
        )

        plain_message = strip_tags(message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [invitation.receiver_email],
            fail_silently=False,
            html_message=message,
        )


class AcceptInvitationView(generics.UpdateAPIView):
    serializer_class = InvitationSerializer

    def update(self, request, *args, **kwargs):
        invitation = get_object_or_404(
            Invitation, id=self.kwargs["invitation_id"], receiver=request.user
        )
        invitation.accepted = True
        invitation.save()
        TeamMember.objects.create(
            team=invitation.team, user=request.user, is_confirmed=True
        )
        return Response(
            {"detail": "You have joined the team."}, status=status.HTTP_200_OK
        )


class RegisterTeamView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        team = get_object_or_404(Team, id=self.kwargs["team_id"], leader=request.user)
        if team.is_registration_complete():
            team.register_team()
            return Response(
                {"detail": "Team successfully registered for the hackathon!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "All team members must confirm their participation."},
            status=status.HTTP_400_BAD_REQUEST,
        )
