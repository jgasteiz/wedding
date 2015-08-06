from django import forms

from .constants import LANGUAGES, INVITATION_STATUSES, INVITER_CHOICES


class InviteeForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGES, required=False)
    invitation_status = forms.ChoiceField(choices=INVITATION_STATUSES, required=False)
    inviter = forms.ChoiceField(choices=INVITER_CHOICES, required=False)

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'invitation_sent', 'language', 'invitation_status', 'inviter')
        model = Invitee


class SongForm(forms.ModelForm):
    name = forms.CharField(label='Song title')
    artist = forms.CharField(label='Artist name', required=False)

    class Meta:
        fields = ('name', 'artist',)
        model = Song


class InvitationEmailForm(forms.ModelForm):
    email_language = forms.ChoiceField(choices=LANGUAGES)

    class Meta:
        fields = ('email_language', 'html',)
        model = InvitationEmail
