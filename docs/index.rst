django-entity-event-slack Documentation
=======================================

Django Entity Event Slack provides a pushable Slack medium for `Django-Entity-Event`_.

.. _`Django-Entity-Event`: https://github.com/ambitioninc/django-entity-event


Setup
-----
To setup the Slack medium, you must create a Slack medium and associated it with the Slack API token
and channel you want to post to.

.. code:: python

    from entity_event_slack.models import SlackMedium

    slack_medium = SlackMedium.objects.create_slack_medium(
        channel='#my-slack-channel', api_token='my-slack-api-token')

In order for rendering to be performed correctly, context renderers with the appropriate style must be
set up in accordance with the documentation of Django Entity Event. Assuming that your rendering style
is set up, associated it with the slack medium.

.. code:: python

    from entity_event.models import RenderingStyle

    style = RenderingStyle.objects.get(name='my_slack_style')
    slack_medium.rendering_style = style
    slack_medium.save()


Once this is done, subscriptions can be made for sources to the slack medium

.. code:: python

    # Subscribe sources to the slack medium
    from entity_event.models import Source, Subscription

    my_source = Source.objects.get(name='my_source')
    Subscription.objects.create(medium=m, source=my_source)

You will need a Celery task for Django Entity Event Slack. It is called ``SendUnseenSlackNotificationsTask``
and can be configured to run at whatever interval you wish. When this is configured, you will start
receiving Slack notifications. While this task definition was removed from this project to make things more maintainable
for our project team, you'll find the source of the task at the time of writing this below.

.. code:: python

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
