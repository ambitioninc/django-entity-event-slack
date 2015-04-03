from datetime import datetime
from django.test import TestCase
from django_dynamic_fixture import G
from entity_event.models import RenderingStyle, ContextRenderer, Source, Subscription, Event, EventSeen
from freezegun import freeze_time
from mock import patch, call
import slack

from entity_event_slack.models import SlackMedium
from entity_event_slack.tasks import send_unseen_slack_notifications, SendUnseenSlackNotificationsTask


class TestRunWorker(TestCase):
    @patch('entity_event_slack.tasks.send_unseen_slack_notifications', spec_set=True)
    def test_run_worker(self, mock_send_unseen_slack_notifications):
        SendUnseenSlackNotificationsTask().run()
        mock_send_unseen_slack_notifications.assert_called_once_with()


class TestSendUnseenNotifications(TestCase):
    @patch('entity_event_slack.tasks.slack.chat.post_message', spec_set=True)
    def test_no_slack_medium(self, mock_post_message):
        send_unseen_slack_notifications()
        self.assertFalse(mock_post_message.called)

    @patch('entity_event_slack.tasks.slack.chat.post_message', spec_set=True)
    def test_no_entity_event_setup(self, mock_post_message):
        G(SlackMedium, name='slack', api_token='api_token')
        send_unseen_slack_notifications()
        self.assertFalse(mock_post_message.called)
        self.assertEquals(slack.api_token, 'api_token')

    @freeze_time(datetime(2015, 1, 1))
    @patch('entity_event_slack.tasks.slack.chat.post_message', spec_set=True)
    def test_w_basic_entity_event_setup(self, mock_post_message):
        style = G(RenderingStyle)
        source = G(Source)
        slack_medium = G(
            SlackMedium, channel='channel', name='slack', api_token='api_token', rendering_style=style,
            icon_url='icon_url', username='user')
        G(ContextRenderer, rendering_style=style, source=source, html_template='You did it!')
        G(Subscription, medium=slack_medium, source=source, only_following=False)

        G(Event, time=datetime(2015, 1, 2), context={}, source=source)

        send_unseen_slack_notifications()

        self.assertEquals(slack_medium.creation_time, datetime(2015, 1, 1))
        self.assertEquals(mock_post_message.call_args_list, [
            call('channel', 'You did it!', icon_url='icon_url', username='user')
        ])
        self.assertEquals(slack.api_token, 'api_token')
        self.assertEquals(EventSeen.objects.count(), 1)

    @freeze_time(datetime(2015, 1, 1))
    @patch('entity_event_slack.tasks.slack.chat.post_message', spec_set=True)
    def test_w_basic_entity_event_setup_preexisting_event(self, mock_post_message):
        style = G(RenderingStyle)
        source = G(Source)
        slack_medium = G(
            SlackMedium, channel='channel', name='slack', api_token='api_token', rendering_style=style,
            icon_url='icon_url', username='user')
        G(ContextRenderer, rendering_style=style, source=source, html_template='You did it!')
        G(Subscription, medium=slack_medium, source=source, only_following=False)

        G(Event, time=datetime(2014, 1, 2), context={}, source=source)

        send_unseen_slack_notifications()

        self.assertEquals(slack_medium.creation_time, datetime(2015, 1, 1))
        self.assertFalse(mock_post_message.called)
        self.assertEquals(slack.api_token, 'api_token')
        self.assertEquals(EventSeen.objects.count(), 0)

    @freeze_time(datetime(2015, 1, 1))
    @patch('entity_event_slack.tasks.slack.chat.post_message', spec_set=True)
    def test_w_basic_entity_multiple_event_setup(self, mock_post_message):
        style = G(RenderingStyle)
        source = G(Source)
        slack_medium = G(
            SlackMedium, icon_url='icon_url', channel='channel', name='slack', api_token='api_token',
            rendering_style=style, username='user')
        G(ContextRenderer, rendering_style=style, source=source, html_template='You did it!')
        G(Subscription, medium=slack_medium, source=source, only_following=False)

        G(Event, time=datetime(2015, 1, 2), context={}, source=source)
        G(Event, time=datetime(2015, 1, 2), context={}, source=source)

        send_unseen_slack_notifications()

        self.assertEquals(slack_medium.creation_time, datetime(2015, 1, 1))
        self.assertEquals(mock_post_message.call_args_list, [
            call('channel', 'You did it!\nYou did it!', icon_url='icon_url', username='user'),
        ])
        self.assertEquals(slack.api_token, 'api_token')
        self.assertEquals(EventSeen.objects.count(), 2)
