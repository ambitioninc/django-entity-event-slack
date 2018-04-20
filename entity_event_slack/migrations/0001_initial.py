# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity_event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlackMedium',
            fields=[
                ('medium_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, serialize=False, to='entity_event.Medium', auto_created=True, primary_key=True, parent_link=True)),
                ('api_token', models.TextField()),
                ('channel', models.TextField()),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('icon_url', models.TextField(default='')),
                ('username', models.TextField(default='')),
            ],
            options={
            },
            bases=('entity_event.medium',),
        ),
    ]
