from django.db import models
from django.conf import settings

from syntaq_auth.models import CustomUserModel


# Create your models here.
class Hackathon(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    organizerId = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    registrationOpen = models.DateTimeField()
    registrationClose = models.DateTimeField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.CharField(max_length=100, null=True, blank=True)
    maxTeamSize = models.IntegerField()
    minTeamSize = models.IntegerField()

    def __str__(self):
        return self.title
