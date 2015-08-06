from django.db import models

from .constants import LANGUAGES


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
    invitation_sent = models.NullBooleanField(default=False)
    language = models.CharField(max_length=256)
    invitation_status = models.CharField(max_length=256)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    inviter = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class InvitationEmail(models.Model):
    email_language = models.CharField(max_length=256)
    html = models.TextField()

    def __unicode__(self):
        return 'Invitation email in {} language'.format(self.email_language)