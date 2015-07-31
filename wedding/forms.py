from django import forms

from .models import InvitationEmail, Invitee, Song

COUNTRIES = (
    ('spain', 'Spain'),
    ('uk', 'United Kingdom'),
    ('poland', 'Poland'),
)

INVITATION_STATUSES = (
    ('no_rsvp', 'No RSVP'),
)

INVITER_CHOICES = (
    ('both', 'Both'),
    ('javi', 'Javi'),
    ('magda', 'Magda'),
)


class InviteeForm(forms.ModelForm):
    country = forms.ChoiceField(choices=COUNTRIES, required=False)
    invitation_status = forms.ChoiceField(choices=INVITATION_STATUSES, required=False)
    inviter = forms.ChoiceField(choices=INVITER_CHOICES, required=False)

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'invitation_sent', 'country', 'invitation_status', 'inviter')
        model = Invitee


class SongForm(forms.ModelForm):
    name = forms.CharField(label='Song title')
    artist = forms.CharField(label='Artist name', required=False)

    class Meta:
        fields = ('name', 'artist',)
        model = Song


class InvitationEmailForm(forms.ModelForm):
    email_language = forms.CharField()

    class Meta:
        fields = ('email_language', 'html',)
        model = InvitationEmail
