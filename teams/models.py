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

    class Meta:
        unique_together = ("hackathon", "leader")

    def is_registration_complete(self):
        return self.members.filter(is_confirmed=False).count() == 0

    def register_team(self):
        if self.is_registration_complete():
            # self.hackathon.registered_teams.add(self)
            # proceed with registration logic
            pass
        else:
            raise ValidationError("Team registration is incomplete")

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
    sender = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, related_name="sent_invitations"
    )
    receiver = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, related_name="received_invitations"
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("team", "receiver")
        constraints = [
            CheckConstraint(
                check=~Q(sender=F("receiver")),
                name="cannot_invite_self",
            ),
        ]

    def __str__(self):
        return f"Invite from {self.sender.username} to {self.receiver.username} for {self.team.name}"
