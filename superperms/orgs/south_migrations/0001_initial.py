# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


# hacky way to support custom AUTH_USER_MODEL
# from this blog post: http://kevindias.com/writing/django-custom-user-models-south-and-reusable-apps/

# Safe User import for Django < 1.5
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()

# With the default User model these will be 'auth.User' and 'auth.user'
# so instead of using orm['auth.User'] we can use orm[user_orm_label]
user_orm_label = '{0}.{1}'.format(User._meta.app_label, User._meta.object_name)
user_model_label = '{0}.{1}'.format(User._meta.app_label, User._meta.module_name)


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExportableField'
        db.create_table(u'orgs_exportablefield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field_model', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='exportable_fields', to=orm['orgs.Organization'])),
        ))
        db.send_create_signal(u'orgs', ['ExportableField'])

        # Adding unique constraint on 'ExportableField', fields ['field_model', 'name', 'organization']
        db.create_unique(u'orgs_exportablefield', ['field_model', 'name', 'organization_id'])

        # Adding model 'OrganizationUser'
        db.create_table(u'orgs_organizationuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[user_orm_label])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orgs.Organization'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=12)),
            ('role_level', self.gf('django.db.models.fields.IntegerField')(default=20)),
        ))
        db.send_create_signal(u'orgs', ['OrganizationUser'])

        # Adding model 'Organization'
        db.create_table(u'orgs_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent_org', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child_orgs', null=True, to=orm['orgs.Organization'])),
            ('query_threshold', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
        ))
        db.send_create_signal(u'orgs', ['Organization'])


    def backwards(self, orm):
        # Removing unique constraint on 'ExportableField', fields ['field_model', 'name', 'organization']
        db.delete_unique(u'orgs_exportablefield', ['field_model', 'name', 'organization_id'])

        # Deleting model 'ExportableField'
        db.delete_table(u'orgs_exportablefield')

        # Deleting model 'OrganizationUser'
        db.delete_table(u'orgs_organizationuser')

        # Deleting model 'Organization'
        db.delete_table(u'orgs_organization')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        user_model_label: {
            'Meta': {
                'object_name': User.__name__,
                'db_table': "'{0}'".format(User._meta.db_table)
            },
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            User._meta.pk.attname: (
                'django.db.models.fields.AutoField', [],
                {
                    'primary_key': 'True',
                    'db_column': "'{0}'".format(User._meta.pk.column)
                },
            ),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'orgs.exportablefield': {
            'Meta': {'ordering': "['organization', 'name']", 'unique_together': "(('field_model', 'name', 'organization'),)", 'object_name': 'ExportableField'},
            'field_model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exportable_fields'", 'to': u"orm['orgs.Organization']"})
        },
        u'orgs.organization': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_org': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_orgs'", 'null': 'True', 'to': u"orm['orgs.Organization']"}),
            'query_threshold': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'users': (
                'django.db.models.fields.related.ManyToManyField', [],
                {
                    'related_name': "'orgs'",
                    'symmetrical': 'False',
                    'through': u"orm['orgs.OrganizationUser']",
                    'to': u"orm['{0}']".format(user_orm_label)
                },
            )
        },
        u'orgs.organizationuser': {
            'Meta': {'ordering': "['organization', '-role_level']", 'object_name': 'OrganizationUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orgs.Organization']"}),
            'role_level': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '12'}),
            'user': ('django.db.models.fields.related.ForeignKey', [],
                     {'to': u"orm['{0}']".format(user_orm_label)},)
        }
    }

    complete_apps = ['orgs']
