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

A Celery task is provided with Django Entity Event Slack. It is called ``SendUnseenSlackNotificationsTask``
and can be configured to run at whatever interval you wish. When this is configured, you will start
receiving Slack notifications.
