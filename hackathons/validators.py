from rest_framework import serializers
from datetime import datetime
from pytz import timezone

from datetime import datetime
from pytz import timezone
from rest_framework import serializers


def validate_dates(data, method, instance=None):
    now = datetime.now().astimezone(timezone("UTC"))

    # Helper function to check if a field was changed
    def is_changed(field):
        if instance:  # If we are updating an existing instance
            return data.get(field) != getattr(instance, field)
        return True  # For POST requests, assume all fields are "changed"

    # Start date validation
    if "start_date" in data and is_changed("start_date"):
        if data["start_date"] < now:
            raise serializers.ValidationError(
                {"start_date": "Start date cannot be before the current time."}
            )

    # End date validation
    if "end_date" in data and is_changed("end_date"):
        if data["end_date"] < now:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be before the current time."}
            )

    # Registration open date validation (only on POST or if it's changed)
    if method == "POST" or (
        "registrationOpen" in data and is_changed("registrationOpen")
    ):
        if data["registrationOpen"] < now:
            raise serializers.ValidationError(
                {
                    "registrationOpen": "Registration open date cannot be before the current time."
                }
            )

    # Registration close date validation
    if "registrationClose" in data and is_changed("registrationClose"):
        if data["registrationClose"] < now:
            raise serializers.ValidationError(
                {
                    "registrationClose": "Registration close date cannot be before the current time."
                }
            )

    # Ensure start_date is not after end_date, if both were changed
    if (
        "start_date" in data
        and "end_date" in data
        and is_changed("start_date")
        and is_changed("end_date")
    ):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError(
                {"start_date": "Start date cannot be after the end date."}
            )

    # Ensure registrationOpen is not after registrationClose, if both were changed
    if (
        "registrationOpen" in data
        and "registrationClose" in data
        and is_changed("registrationOpen")
        and is_changed("registrationClose")
    ):
        if data["registrationOpen"] > data["registrationClose"]:
            raise serializers.ValidationError(
                {
                    "registrationOpen": "Registration open date cannot be after the registration close date."
                }
            )

    # Ensure start_date is not before registrationOpen, if both were changed
    if (
        "start_date" in data
        and "registrationOpen" in data
        and is_changed("start_date")
        and is_changed("registrationOpen")
    ):
        if data["start_date"] < data["registrationOpen"]:
            raise serializers.ValidationError(
                {
                    "start_date": "Start date cannot be before the registration open date."
                }
            )

    # Ensure end_date is not before registrationOpen, if both were changed
    if (
        "end_date" in data
        and "registrationOpen" in data
        and is_changed("end_date")
        and is_changed("registrationOpen")
    ):
        if data["end_date"] < data["registrationOpen"]:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be before the registration open date."}
            )

    # Ensure end_date is not before registrationClose, if both were changed
    if (
        "end_date" in data
        and "registrationClose" in data
        and is_changed("end_date")
        and is_changed("registrationClose")
    ):
        if data["end_date"] < data["registrationClose"]:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be before the registration close date."}
            )

    # Ensure start_date is not before registrationClose, if both were changed
    if (
        "start_date" in data
        and "registrationClose" in data
        and is_changed("start_date")
        and is_changed("registrationClose")
    ):
        if data["start_date"] < data["registrationClose"]:
            raise serializers.ValidationError(
                {
                    "start_date": "Start date cannot be before the registration close date."
                }
            )

    return data  # Return the validated data


def validate_team_size(data):
    if data["maxTeamSize"] < data["minTeamSize"]:
        raise serializers.ValidationError(
            {"maxTeamSize": "Max team size cannot be less than min team size."}
        )
