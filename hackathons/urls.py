from django.urls import path
from . import views

urlpatterns = [
    # path("", views.api_home),
    path("", views.hackathon_list_create_view),
    path(
        "organized-hackathons/",
        views.OrganizerHackathonView.as_view(),
        name="organized-hackathons",
    ),
    path(
        "participated-hackathons/",
        views.ParticipatedHackathonView.as_view(),
        name="participated-hackathons",
    ),
    path("<int:pk>/", views.hackathon_detail_update_destroy_view),
    # path(
    #     "<int:pk>/",
    #     views.HackathonUpdateAPIView.as_view(),
    #     name="update-hackathon",
    # ),
    path("<int:pk>/user-team/", views.UserTeamView.as_view(), name="user-team"),
]
