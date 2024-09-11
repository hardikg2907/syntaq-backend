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
        "<int:team_id>/members/",
        views.TeamMembersListAPIView.as_view(),
        name="team_members_list",
    ),
    path(
        "members/<int:pk>/",
        views.TeamMembersDeleteAPIView.as_view(),
        name="team_members_delete",
    ),
    path(
        "members-and-invitations/<int:team_id>/",
        views.TeamMembersAndInvitationsListView.as_view(),
        name="team_members",
    ),
    path(
        "invitations/<str:pk>",
        views.InvitationDetailAPIView.as_view(),
        name="invitations_detail",
    ),
    path(
        "invitations/<int:team_id>/",
        views.SendInvitationView.as_view(),
        name="send_invitation",
    ),
    path(
        "invitations/<str:pk>/",
        views.InvitationDeleteAPIView.as_view(),
        name="delete_invitation",
    ),
    path(
        "invitations/accept/<str:invitation_id>/",
        views.AcceptInvitationView.as_view(),
        name="accept_invitation",
    ),
    path(
        "register/<int:team_id>/",
        views.RegisterTeamView.as_view(),
        name="register_team",
    ),
]
