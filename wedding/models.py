from django.db import models

from .constants import LANGUAGES, NO_RSVP


class Song(models.Model):
    name = models.CharField(max_length=256)
    artist = models.CharField(max_length=256, blank=True)
    submitted_by = models.CharField(max_length=256, blank=True)
    is_approved = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-added',)

    def __unicode__(self):
        return '{}, by {} - submitted by {}'.format(self.name, self.artist, self.submitted_by)

    def save(self, *args, **kwars):
        self.artist = self.artist.capitalize()
        super(Song, self).save()


class Invitee(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True)
    email = models.EmailField(blank=True)
    language = models.CharField(max_length=256)
    invitation_status = models.CharField(max_length=256, default=NO_RSVP)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    inviter = models.CharField(max_length=256, blank=True)

    has_plusone = models.NullBooleanField(default=False)

    emails = models.CommaSeparatedIntegerField(max_length=512)

    class Meta:
        ordering = ('first_name', 'last_name',)

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_emails(self):
        """
        Return the list of Email instances that have been sent to the invitee.
        """
        email_ids = self.get_email_ids()
        Email = get_email_class()
        return [email for email in Email.objects.filter(pk__in=email_ids)]

    def get_email_ids(self):
        """
        Return the list of Email ids that have been sent to the invitee.
        """
        if self.emails is None or self.emails == '':
            return []
        email_ids = self.emails.replace(' ', '')
        return email_ids.split(',')


def create_model(name, fields=None, app_label='', module='', options=None):
    """
    Create specified model
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    return model


def get_email_class():
    fields = {
        'name': models.CharField(max_length=256),
        '__unicode__': lambda self: self.name
    }
    options = {
        'ordering': ['name'],
    }
    for language_key, language_name in LANGUAGES:
        fields['html_{}'.format(language_key)] = models.TextField(blank=True, null=True)
    return create_model('Email', fields, 'wedding', options=options)
