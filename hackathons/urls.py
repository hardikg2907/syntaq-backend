from django.urls import path
from . import views

urlpatterns = [
    # path("", views.api_home),
    path("", views.hackathon_list_create_view),
    path("<int:pk>/", views.hackathon_detail_view),
    path("<int:pk>/user-team/", views.UserTeamView.as_view(), name="user-team"),
]
