from django.test import TestCase
from django_dynamic_fixture import G
from mock import patch
import slack

from entity_event_slack.models import SlackMedium
from entity_event_slack.tasks import send_unseen_slack_notifications


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
