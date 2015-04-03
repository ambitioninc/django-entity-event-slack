# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SlackMedium.icon_url'
        db.add_column(u'entity_event_slack_slackmedium', 'icon_url',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'SlackMedium.username'
        db.add_column(u'entity_event_slack_slackmedium', 'username',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SlackMedium.icon_url'
        db.delete_column(u'entity_event_slack_slackmedium', 'icon_url')

        # Deleting field 'SlackMedium.username'
        db.delete_column(u'entity_event_slack_slackmedium', 'username')


    models = {
        u'entity_event.medium': {
            'Meta': {'object_name': 'Medium'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'rendering_style': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_event.RenderingStyle']", 'null': 'True'})
        },
        u'entity_event.renderingstyle': {
            'Meta': {'object_name': 'RenderingStyle'},
            'display_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'entity_event_slack.slackmedium': {
            'Meta': {'object_name': 'SlackMedium', '_ormbases': [u'entity_event.Medium']},
            'api_token': ('django.db.models.fields.TextField', [], {}),
            'channel': ('django.db.models.fields.TextField', [], {}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'icon_url': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'medium_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['entity_event.Medium']", 'unique': 'True', 'primary_key': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['entity_event_slack']