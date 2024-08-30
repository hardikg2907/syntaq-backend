from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from hackathons.models import Hackathon
from syntaq_auth.models import CustomUserModel
from syntaq_auth.views import get_user
from .models import Team, Invitation, TeamMember
from .serializers import TeamSerializer, InvitationSerializer, TeamMemberSerializer


class CreateTeamView(generics.CreateAPIView):
    serializer_class = TeamSerializer
    # permission_classes = [IsAuthenticated]

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
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        team = get_object_or_404(Team, id=self.kwargs["team_id"])
        friend = get_object_or_404(
            CustomUserModel, id=self.request.data.get("friend_id")
        )
        serializer.save(team=team, sender=self.request.user, receiver=friend)


class AcceptInvitationView(generics.UpdateAPIView):
    serializer_class = InvitationSerializer
    # permission_classes = [IsAuthenticated]

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
