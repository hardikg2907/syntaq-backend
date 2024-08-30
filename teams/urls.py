from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateTeamView.as_view(), name="create_team"),
]
