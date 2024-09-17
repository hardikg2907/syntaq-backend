from rest_framework import serializers
from datetime import datetime
from pytz import timezone


def validate_dates(data, method):
    now = datetime.now().astimezone(timezone("UTC"))

    if data["start_date"] < now:
        raise serializers.ValidationError(
            {"start_date": "Start date cannot be before current time."}
        )
    if data["end_date"] < now:
        raise serializers.ValidationError(
            {"end_date": "End date cannot be before current time."}
        )
    if method == "POST":
        if data["registrationOpen"] < now:
            raise serializers.ValidationError(
                {
                    "registrationOpen": "Registration open date cannot be before current time."
                }
            )
    if data["registrationClose"] < now:
        raise serializers.ValidationError(
            {
                "registrationClose": "Registration close date cannot be before current time."
            }
        )

    if data["start_date"] > data["end_date"]:
        raise serializers.ValidationError(
            {"start_date": "Start date cannot be after end date."}
        )
    if data["registrationOpen"] > data["registrationClose"]:
        raise serializers.ValidationError(
            {
                "registrationOpen": "Registration open date cannot be after registration close date."
            }
        )
    if data["start_date"] < data["registrationOpen"]:
        raise serializers.ValidationError(
            {"start_date": "Start date cannot be before registration open date."}
        )
    if data["end_date"] < data["registrationOpen"]:
        raise serializers.ValidationError(
            {"end_date": "End date cannot be before registration open date."}
        )
    if data["end_date"] < data["registrationClose"]:
        raise serializers.ValidationError(
            {"end_date": "End date cannot be before registration close date."}
        )
    if data["start_date"] < data["registrationClose"]:
        raise serializers.ValidationError(
            {"start_date": "Start date cannot be before registration close date."}
        )


def validate_team_size(data):
    if data["maxTeamSize"] < data["minTeamSize"]:
        raise serializers.ValidationError(
            {"maxTeamSize": "Max team size cannot be less than min team size."}
        )
