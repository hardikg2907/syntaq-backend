from django.urls import path, include
from . import views

urlpatterns = [
    path("team/<int:team_id>", views.TeamInfoView.as_view(), name="team_info")
]
