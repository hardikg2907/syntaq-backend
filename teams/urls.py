from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateTeamView.as_view(), name="create_team"),
    path(
        "<int:team_id>/invite/",
        views.SendInvitationView.as_view(),
        name="send_invitation",
    ),
    path(
        "<int:team_id>/accept/<str:invitation_id>/",
        views.AcceptInvitationView.as_view(),
        name="accept_invitation",
    ),
]
