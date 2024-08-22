from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def api_home(request, *args, **kwargs):

    return Response({"message": "Hello, world!"})