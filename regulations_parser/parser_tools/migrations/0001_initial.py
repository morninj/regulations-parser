# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Regulation'
        db.create_table('parser_tools_regulation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(default='[Not set]', max_length=255)),
            ('parent_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('media', self.gf('django.db.models.fields.CharField')(default='PDF', max_length=255)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(default='MA', max_length=100)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('parser_tools', ['Regulation'])

        # Adding model 'Page'
        db.create_table('parser_tools_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regulation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parser_tools.Regulation'])),
            ('page_number', self.gf('django.db.models.fields.IntegerField')()),
            ('contents', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('parser_tools', ['Page'])

        # Adding model 'Incorporation'
        db.create_table('parser_tools_incorporation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parser_tools.Page'])),
            ('standard', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('context', self.gf('django.db.models.fields.TextField')()),
            ('context_start_position', self.gf('django.db.models.fields.IntegerField')()),
            ('context_end_position', self.gf('django.db.models.fields.IntegerField')()),
            ('standards_organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parser_tools.StandardsOrganization'], null=True, blank=True)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_incorporation', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('parser_tools', ['Incorporation'])

        # Adding model 'StandardsOrganization'
        db.create_table('parser_tools_standardsorganization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('parser_tools', ['StandardsOrganization'])


    def backwards(self, orm):
        # Deleting model 'Regulation'
        db.delete_table('parser_tools_regulation')

        # Deleting model 'Page'
        db.delete_table('parser_tools_page')

        # Deleting model 'Incorporation'
        db.delete_table('parser_tools_incorporation')

        # Deleting model 'StandardsOrganization'
        db.delete_table('parser_tools_standardsorganization')


    models = {
        'parser_tools.incorporation': {
            'Meta': {'object_name': 'Incorporation'},
            'context': ('django.db.models.fields.TextField', [], {}),
            'context_end_position': ('django.db.models.fields.IntegerField', [], {}),
            'context_start_position': ('django.db.models.fields.IntegerField', [], {}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_incorporation': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parser_tools.Page']"}),
            'standard': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'standards_organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parser_tools.StandardsOrganization']", 'null': 'True', 'blank': 'True'})
        },
        'parser_tools.page': {
            'Meta': {'object_name': 'Page'},
            'contents': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_number': ('django.db.models.fields.IntegerField', [], {}),
            'regulation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parser_tools.Regulation']"})
        },
        'parser_tools.regulation': {
            'Meta': {'object_name': 'Regulation'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.CharField', [], {'default': "'PDF'", 'max_length': '255'}),
            'parent_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'MA'", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'[Not set]'", 'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'parser_tools.standardsorganization': {
            'Meta': {'ordering': "['acronym']", 'object_name': 'StandardsOrganization'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['parser_tools']