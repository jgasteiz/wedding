from django.db import models
from django.core.signing import Signer

from settings import SECRET_KEY
from .utils import AESCipher


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
    country = models.CharField(max_length=256)
    invitation_status = models.CharField(max_length=256)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    inviter = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class EmailCredentials(models.Model):
    email_address = models.EmailField()
    password = models.CharField(max_length=256)

    def __unicode__(self):
        return self.email_address

    @classmethod
    def get_instance(cls):
        instance, _ = cls.objects.get_or_create(id=1)
        return instance

    def get_password(self):
        cipher = AESCipher(SECRET_KEY)
        return cipher.decrypt(self.password)

    def delete(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        self.id = 1
        cipher = AESCipher(SECRET_KEY)
        self.password = cipher.encrypt(self.password)
        super(EmailCredentials, self).save(*args, **kwargs)