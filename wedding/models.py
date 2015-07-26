from django.db import models


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
