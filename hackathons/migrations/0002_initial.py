# Generated by Django 5.1 on 2024-08-30 17:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("hackathons", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="hackathon",
            name="organizerId",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddConstraint(
            model_name="hackathon",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("registrationClose__gte", models.F("registrationOpen"))
                ),
                name="registration_close_gte_registration_open",
            ),
        ),
        migrations.AddConstraint(
            model_name="hackathon",
            constraint=models.CheckConstraint(
                condition=models.Q(("end_date__gte", models.F("start_date"))),
                name="end_date_gte_start_date",
            ),
        ),
        migrations.AddConstraint(
            model_name="hackathon",
            constraint=models.CheckConstraint(
                condition=models.Q(("maxTeamSize__gte", models.F("minTeamSize"))),
                name="max_team_size_gte_min_team_size",
            ),
        ),
    ]
