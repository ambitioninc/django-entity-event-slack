from django.db import models
from entity_event.models import Medium

from entity_event_slack import constants


class SlackMediumManager(models.Manager):
    def get_queryset(self):
        return super(SlackMediumManager, self).get_queryset().filter(name=constants.SLACK_MEDIUM_NAME)


class SlackMedium(Medium):
    """
    A medium that extends djagno entity event's Medium to include
    Slack-specific configuration.
    """
    # The slack API token
    api_token = models.TextField()

    # The slack channel to post events to
    channel = models.TextField()

    # The time at which this medium was created. Events before this time will never be
    # pushed
    creation_time = models.DateTimeField(auto_now_add=True)

    objects = SlackMediumManager()
