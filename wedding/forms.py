from django import forms

from .models import Song


class SongForm(forms.ModelForm):
    name = forms.CharField(label='Song title')
    artist = forms.CharField(label='Artist name')

    class Meta:
        fields = ('name', 'artist',)
        model = Song
