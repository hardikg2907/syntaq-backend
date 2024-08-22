from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import status

from .models import Hackathon
from .serializers import HackathonSerializer

from syntaq_auth.views import get_user


@api_view(["GET"])
def api_home(request, *args, **kwargs):

    return Response({"message": "Hello, Hackathons!"})


class HackathonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Hackathon.objects.all()

    serializer_class = HackathonSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        user_email = request.data.get("userEmail")
        userId = get_user(user_email)
        print(userId)
        # serializer.save(organizerId=user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, organizerId=userId)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(**kwargs)
        print(self.request.data)


hackathon_list_create_view = HackathonListCreateAPIView.as_view()
