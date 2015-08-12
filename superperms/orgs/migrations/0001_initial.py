# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgjson.fields
from django.conf import settings
import uuidfield.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportableField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_model', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['organization', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', uuidfield.fields.UUIDField(default=uuid.uuid4, unique=True, max_length=32, editable=False, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('config', djorm_pgjson.fields.JSONField(default={}, null=True, blank=True)),
                ('query_threshold', models.IntegerField(max_length=4, null=True, blank=True)),
                ('parent_org', models.ForeignKey(related_name='child_orgs', blank=True, to='orgs.Organization', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OrganizationUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'pending', max_length=12, choices=[(b'pending', b'Pending'), (b'accepted', b'Accepted'), (b'rejected', b'Rejected')])),
                ('role_level', models.IntegerField(default=20, choices=[(0, b'Viewer'), (10, b'Member'), (20, b'Owner')])),
                ('organization', models.ForeignKey(to='orgs.Organization')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['organization', '-role_level'],
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='users',
            field=models.ManyToManyField(related_name='orgs', through='orgs.OrganizationUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exportablefield',
            name='organization',
            field=models.ForeignKey(related_name='exportable_fields', to='orgs.Organization'),
        ),
        migrations.AlterUniqueTogether(
            name='exportablefield',
            unique_together=set([('field_model', 'name', 'organization')]),
        ),
    ]
