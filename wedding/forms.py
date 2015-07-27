from django import forms

from .models import Invitee, Song

COUNTRIES = (
    ('spain', 'Spain'),
    ('uk', 'United Kingdom'),
    ('poland', 'Poland'),
)

INVITATION_STATUSES = (
    ('no_rsvp', 'No RSVP'),
)


class InviteeForm(forms.ModelForm):
    country = forms.ChoiceField(choices=COUNTRIES, required=False)
    invitation_status = forms.ChoiceField(choices=INVITATION_STATUSES, required=False)

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'invitation_sent', 'country', 'invitation_status')
        model = Invitee


class SongForm(forms.ModelForm):
    name = forms.CharField(label='Song title')
    artist = forms.CharField(label='Artist name', required=False)

    class Meta:
        fields = ('name', 'artist',)
        model = Song
