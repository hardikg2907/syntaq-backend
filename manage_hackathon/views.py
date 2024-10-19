from rest_framework import generics, status
from rest_framework.response import Response
from teams.models import Team, Invitation, TeamMember
from teams.serializers import TeamSerializer, InvitationSerializer, TeamMemberSerializer


class TeamInfoView(generics.RetrieveAPIView):
    """
    Fetch and display details of a team, including its members and invitations.
    """

    def get(self, request, *args, **kwargs):
        # Fetch the team by ID and related members and invitations
        team_id = self.kwargs.get("team_id")
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Get all invitations for this team with invited_by relationship optimized
        invitations = Invitation.objects.filter(team=team)

        # Serialize the team, members, and invitations
        team_serializer = TeamSerializer(team)
        member_serializer = TeamMemberSerializer(team.members.all(), many=True)
        invitation_serializer = InvitationSerializer(invitations, many=True)

        # Return a response with serialized data
        return Response(
            {
                **team_serializer.data,
                "members": member_serializer.data,  # Team members information
                "invitations": invitation_serializer.data,  # Invitation information
            },
            status=status.HTTP_200_OK,
        )
