# Generated by Django 5.1 on 2024-08-31 09:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="registered",
            field=models.BooleanField(default=False),
        ),
    ]
