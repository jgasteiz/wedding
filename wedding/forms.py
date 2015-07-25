from django import forms

from .models import Song


class SongForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'artist',)
        model = Song
