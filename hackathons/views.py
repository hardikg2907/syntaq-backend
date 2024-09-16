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


class HackathonDetailAPIView(generics.RetrieveAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    lookup_field = "pk"


hackathon_detail_view = HackathonDetailAPIView.as_view()


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
