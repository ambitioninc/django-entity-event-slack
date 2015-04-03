# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SlackMedium'
        db.create_table(u'entity_event_slack_slackmedium', (
            (u'medium_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['entity_event.Medium'], unique=True, primary_key=True)),
            ('api_token', self.gf('django.db.models.fields.TextField')()),
            ('channel', self.gf('django.db.models.fields.TextField')()),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'entity_event_slack', ['SlackMedium'])


    def backwards(self, orm):
        # Deleting model 'SlackMedium'
        db.delete_table(u'entity_event_slack_slackmedium')


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
            u'medium_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['entity_event.Medium']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['entity_event_slack']