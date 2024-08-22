from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

from .models import Hackathon
from .serializers import HackathonSerializer


@api_view(["GET"])
def api_home(request, *args, **kwargs):

    return Response({"message": "Hello, Hackathons!"})

class HackathonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Hackathon.objects.all()

    serializer_class = HackathonSerializer

    def perform_create(self, serializer):
        serializer.save(organizerId=self.request.user)

hackathon_list_create_view = HackathonListCreateAPIView.as_view()
