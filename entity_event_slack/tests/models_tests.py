from django.test import TestCase

from entity_event_slack.models import SlackMedium


class SlackMediumManagerTest(TestCase):
    def test_create_slack_medium_no_existing(self):
        m = SlackMedium.objects.create_slack_medium(channel='#slack-channel', api_token='api_token')

        self.assertEquals(m.channel, '#slack-channel')
        self.assertEquals(m.api_token, 'api_token')

    def test_create_slack_medium_w_existing(self):
        m = SlackMedium.objects.create_slack_medium(channel='#slack-channel', api_token='api_token')
        m = SlackMedium.objects.create_slack_medium(channel='new channel', api_token='new api token')

        # Medium should not have been updated on second creation
        self.assertEquals(m.channel, '#slack-channel')
        self.assertEquals(m.api_token, 'api_token')
