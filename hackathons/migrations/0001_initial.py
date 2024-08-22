# Generated by Django 5.1 on 2024-08-22 08:47

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Hackathon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("subtitle", models.CharField(max_length=100, null=True)),
                ("description", models.TextField(null=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("registrationOpen", models.DateField()),
                ("registrationClose", models.DateField()),
                ("location", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("photo", models.CharField(max_length=100, null=True)),
                ("maxTeamSize", models.IntegerField()),
                ("minTeamSize", models.IntegerField()),
            ],
        ),
    ]
