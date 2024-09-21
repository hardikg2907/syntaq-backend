from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import status
from datetime import datetime
from pytz import timezone

from .models import Hackathon
from .serializers import HackathonSerializer

from syntaq_auth.views import get_user
from teams.models import Team, TeamMember

from teams.serializers import TeamSerializer


@api_view(["GET"])
def api_home(request, *args, **kwargs):

    return Response({"message": "Hello, Hackathons!"})


class HackathonListCreateAPIView(generics.ListCreateAPIView):
    now = datetime.now().astimezone(timezone("UTC"))

    queryset = Hackathon.objects.filter(registrationClose__gte=now)

    serializer_class = HackathonSerializer

    def create(self, request, *args, **kwargs):
        # serializer.save(organizerId=user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, organizerId=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(**kwargs)
        # print(self.request.data)


hackathon_list_create_view = HackathonListCreateAPIView.as_view()


class HackathonDetailUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        # user = request.user
        # if not user:
        #     return Response(
        #         {"error": "You must be logged in to update a hackathon"},
        #         status=status.HTTP_401_UNAUTHORIZED,
        #     )
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            old_data = serializer.to_representation(instance)
            # if instance.organizerId != user:
            #     return Response(
            #         {"error": "You are not authorized to update this hackathon"},
            #         status=status.HTTP_403_FORBIDDEN,
            #     )
            updated_data = {**old_data, **request.data}
            serializer = self.get_serializer(instance, data=updated_data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response({"error": e}, status=500)


hackathon_detail_update_destroy_view = HackathonDetailUpdateDestroyAPIView.as_view()


class UserTeamView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        hackathon_id = self.kwargs.get("pk")
        user = request.user

        try:
            team_member = (
                TeamMember.objects.select_related("team")
                .filter(user=user, team__hackathon_id=hackathon_id)
                .first()
            )
            if team_member:
                team = team_member.team
                return Response(
                    {
                        "team_name": team.name,
                    }
                )
            else:
                return Response(None)

        except Exception as e:
            # Log the error and return a 500 Internal Server Error response
            print(f"Error occurred: {e}")
            return Response({"error": e}, status=500)


class OrganizerHackathonView(generics.ListAPIView):
    serializer_class = HackathonSerializer

    def get_queryset(self):
        user = self.request.user
        return Hackathon.objects.filter(organizerId=user).order_by("-created_at")


class ParticipatedHackathonView(generics.ListAPIView):
    serializer_class = HackathonSerializer

    def get_queryset(self):
        user = self.request.user
        return (
            Hackathon.objects.prefetch_related("teams__members")
            .filter(teams__members__user=user)
            .distinct()
            .order_by("-created_at")
        )


class HackathonRegistrationsAPIView(generics.ListAPIView):
    serializer_class = TeamSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        hackathon_id = kwargs.get("pk")
        hackathon = Hackathon.objects.get(id=hackathon_id)
        print(hackathon)
        if hackathon.organizerId != user:
            return Response(
                {"error": "You are not authorized to view this page"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        hackathon_id = self.kwargs.get("pk")
        return Team.objects.filter(hackathon_id=hackathon_id).order_by("-created_at")
