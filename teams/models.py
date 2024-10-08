from django.db import models
from django.db.models import CheckConstraint, Q, F
from uuid import uuid4
from django.core.exceptions import ValidationError

from hackathons.models import Hackathon
from syntaq_auth.models import CustomUserModel


class Team(models.Model):
    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="teams"
    )
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, related_name="led_teams"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    registration_complete = models.BooleanField(default=False)

    class Meta:
        unique_together = ("hackathon", "leader")

    def is_valid(self):
        """
        Check if the team's registration is complete and validation.
        Returns:
            bool: True if the team's registration is complete and valid composition, False otherwise.
        """
        members_count = self.members.count()
        invitations_count = self.invitations.count()
        if (
            members_count < self.hackathon.minTeamSize
            or members_count > self.hackathon.maxTeamSize
            or invitations_count != 0
        ):
            # raise ValidationError("Team size is not within the hackathon's limits")
            return False
        return True

    def register_team(self):
        self.registration_complete = True
        self.save()

    def __str__(self):
        return f"{self.name} - {self.hackathon.title}"


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, related_name="team_memberships"
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("team", "user")
        # constraints = [
        #     CheckConstraint(
        #         check=Q(team__hackathon__registrationClose__gte=F('joined_at')),
        #         name="member_join_within_registration_period",
        #     ),
        # ]

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"


class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="invitations")
    # receiver = models.ForeignKey(
    #     CustomUserModel, on_delete=models.CASCADE, related_name="received_invitations"
    # )
    receiver_email = models.EmailField(null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("team", "receiver_email")
        # constraints = [
        #     CheckConstraint(
        #         check=~Q(sender=F("receiver")),
        #         name="cannot_invite_self",
        #     ),
        # ]

    def __str__(self):
        return f"Invite  to {self.receiver_email} for {self.team.name}"
