from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import CheckConstraint, Q, F

from syntaq_auth.models import CustomUserModel


# Create your models here.
class Hackathon(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    organizerId = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, related_name="organized_hackathons"
    )

    registrationOpen = models.DateTimeField()
    registrationClose = models.DateTimeField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.CharField(max_length=100, null=True, blank=True)
    maxTeamSize = models.IntegerField()
    minTeamSize = models.IntegerField()

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(registrationClose__gte=F("registrationOpen")),
                name="registration_close_gte_registration_open",
            ),
            CheckConstraint(
                check=Q(end_date__gte=F("start_date")), name="end_date_gte_start_date"
            ),
            CheckConstraint(
                check=Q(maxTeamSize__gte=F("minTeamSize")),
                name="max_team_size_gte_min_team_size",
            ),
        ]

    def __str__(self):
        return self.title
