from django.db import models
from django.conf import settings
from django.template import loader, Context

from .constants import (
    NO_RSVP,
    INVITATION_STATUSES,
    INVITER_CHOICES,
    EMAIL_BASE_TEMPLATE,
)


class Song(models.Model):
    """
    Model for storing the submitted songs by the invitees.
    """
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
    """
    Model for storing information about the wedding invitees.
    """
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

    def get_invitation_status(self):
        return dict(INVITATION_STATUSES).get(self.invitation_status)

    def get_language(self):
        return dict(settings.LANGUAGES).get(self.language)

    def get_inviter(self):
        return dict(INVITER_CHOICES).get(self.inviter)


def create_model(name, fields=None, app_label='', module='', options=None):
    """
    Create specified model

    :param name: name of the dynamic model
    :param fields: fields the model should have
    :param app_label: app_label the model should have
    :param module: module of the model
    :param options: extra options for the model Meta.
    :return:
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
    """
    Returns a dynamic model, Email

    :return: model
    """
    fields = {
        'name': models.CharField(max_length=256),
        '__unicode__': lambda self: self.name
    }
    options = {
        'ordering': ['name'],
    }
    for language_key, language_name in settings.LANGUAGES:
        fields['html_{}'.format(language_key)] = models.TextField(blank=True, null=True)
    return create_model('Email', fields, 'wedding', options=options)


def get_email_content(email, language):
    """
    Given an email instance and a language, returns the rendered html of that
    email in that language.

    :param email: instance of dynamic model Email
    :param language: language in which the email should be rendered
    :return: html text
    """
    email_html = getattr(email, 'html_{}'.format(language))
    template = loader.get_template(EMAIL_BASE_TEMPLATE)
    context = Context({'content': email_html})
    return template.render(context)
