from django.urls import path
from . import views

urlpatterns = [
    path(
        "<int:hackathon_id>/",
        views.UserTeamInHackathonView.as_view(),
        name="team_detail",
    ),
    path("update/<int:pk>/", views.UpdateTeamAPIView.as_view(), name="update_team"),
    path("create/", views.CreateTeamView.as_view(), name="create_team"),
    path(
        "members/<int:team_id>/",
        views.TeamMembersAndInvitationsListView.as_view(),
        name="team_members",
    ),
    path(
        "invitations/<int:team_id>",
        views.InvitationsListView.as_view(),
        name="invitations",
    ),
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
    path(
        "register/<int:team_id>/",
        views.RegisterTeamView.as_view(),
        name="register_team",
    ),
]
