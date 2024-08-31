from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task
from os import getenv


@shared_task
def send_invitation_email(invitation, team):
    frontend_base_url = getenv("FRONTEND_URL")
    # Construct the frontend URL with team_id and invitation_id as query parameters
    accept_url = f"{frontend_base_url}/accept-invitation?teamId={team.id}&invitationId={invitation.id}"
    subject = f"Invitation to join team {team.name} for {team.hackathon.title}"
    leader_full_name = f"{team.leader.first_name} {team.leader.last_name}"
    message = render_to_string(
        "teams/invitation_email.html",
        {
            "team": team,
            "invitation": invitation,
            "accept_url": accept_url,
            "leader_full_name": leader_full_name,
        },
    )
    plain_message = strip_tags(message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [invitation.receiver_email],
        fail_silently=False,
        html_message=message,
    )
