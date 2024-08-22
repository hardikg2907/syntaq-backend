from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # auth.User

# Create your models here.
class Hackathon(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    organizerId = models.ForeignKey(User, on_delete=models.CASCADE)
    registrationOpen = models.DateField()
    registrationClose = models.DateField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.CharField(max_length=100,null=True)
    maxTeamSize = models.IntegerField()
    minTeamSize = models.IntegerField()

    def __str__(self):
        return self.title