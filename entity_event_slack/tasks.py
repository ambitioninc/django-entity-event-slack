from celery import Task
from db_mutex.db_mutex import db_mutex
from manager_utils import get_or_none
import slack
import slack.chat

from entity_event_slack.models import SlackMedium


class SendUnseenSlackNotificationsTask(Task):
    """
    Converts events to emails based on the email subscriptions.
    """
    def run(self, *args, **kwargs):
        with db_mutex('push-slack-events'):
            self.run_worker(*args, **kwargs)

    def run_worker(self, *args, **kwargs):
        send_unseen_slack_notifications()


def send_unseen_slack_notifications():
    """
    Pushes rendered notifications to slack.
    """
    slack_medium = get_or_none(SlackMedium.objects)

    if slack_medium:
        slack.api_token = slack_medium.api_token

        # Gather all events while marking them as seen. Only events after the creation of the slack
        # medium are gathered.
        events = [e for e, targets in slack_medium.events_targets(
            seen=False, mark_seen=True, start_time=slack_medium.creation_time)]

        # Render the events. If rendering fails for any event, no slack notifications will
        # be sent.
        rendered_events = slack_medium.render(events)

        # Try to post them to the configured slack channel. If the post fails, all events will
        # be marked as seen and never sent to slack. This is a safety measure to ensure we dont
        # send duplicate events to slack
        msg = '\n'.join([html for (txt, html) in rendered_events.values()])

        if msg:
            slack.chat.post_message(
                slack_medium.channel, msg, username=slack_medium.username, icon_url=slack_medium.icon_url)
