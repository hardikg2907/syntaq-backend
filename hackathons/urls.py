from django.urls import path
from . import views

urlpatterns = [
    # path("", views.api_home),
    path("", views.hackathon_list_create_view),
]
