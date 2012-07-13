from django.db import models

class Regulation(models.Model):
    parent_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255, default='[Not set]')
    parent_url = models.URLField() # The index page from which this chunk
        # of legislation was downloaded
    url = models.URLField() # The URL of the actual piece of legislation
    media = models.CharField(max_length=255, default='PDF') # Currently can
        # be 'PDF' or 'HTML'
    filename = models.CharField(max_length=255)
    state = models.CharField(max_length=100, default='MA')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return 'Title: ' + self.title + '; Filename: ' + self.filename

class Page(models.Model):
    regulation = models.ForeignKey(Regulation)
    page_number = models.IntegerField()
    contents = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return 'Regulation ' + self.regulation.filename + ', p. ' + str(self.page_number)

class Incorporation(models.Model):
    page = models.ForeignKey(Page)
    standard = models.CharField(max_length=255, blank=True)
    context = models.TextField()
    context_start_position = models.IntegerField()
    context_end_position = models.IntegerField()
    standards_organization = models.ForeignKey('StandardsOrganization', null=True, blank=True)
    edition = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    is_incorporation = models.NullBooleanField(default=None)

class StandardsOrganization(models.Model):
    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=255, blank=False)
    def __unicode__(self):
        return self.acronym + ' (' + self.name + ')'
    class Meta:
        ordering = ['acronym']
