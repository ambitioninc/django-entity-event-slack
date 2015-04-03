from django.db import models
from entity_event.models import Medium

from entity_event_slack import constants


class SlackMediumManager(models.Manager):
    def get_queryset(self):
        return super(SlackMediumManager, self).get_queryset().filter(name=constants.SLACK_MEDIUM_NAME)

    def create_slack_medium(self, **kwargs):
        return self.get_or_create(name=constants.SLACK_MEDIUM_NAME, defaults=kwargs)[0]


class SlackMedium(Medium):
    """
    A medium that extends djagno entity event's Medium to include
    Slack-specific configuration. When this medium is present, events will be pushed to this
    medium using the configured api_token and channel.
    """
    # The slack API token
    api_token = models.TextField()

    # The slack channel to post events to
    channel = models.TextField()

    # The time at which this medium was created. Events before this time will never be
    # pushed
    creation_time = models.DateTimeField(auto_now_add=True)

    # The icon url to use for the bot
    icon_url = models.TextField(default='')

    # The username for this bot
    username = models.TextField(default='')

    objects = SlackMediumManager()
