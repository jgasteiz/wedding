from django import forms
from django.db import models

from .constants import LANGUAGES, INVITATION_STATUSES, INVITER_CHOICES
from django.forms import model_to_dict
from django.utils.translation import ugettext_lazy as _
from .models import Invitee, Song, get_email_class


class InviteeForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGES, required=False)
    invitation_status = forms.ChoiceField(choices=INVITATION_STATUSES, required=False)
    inviter = forms.ChoiceField(choices=INVITER_CHOICES, required=False)

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'email',
            'language',
            'invitation_status',
            'has_plusone',
            'inviter',
        )
        model = Invitee


class SongForm(forms.ModelForm):
    name = forms.CharField(label=_('Song title'))
    artist = forms.CharField(label=_('Artist name'), required=False)

    class Meta:
        fields = ('name', 'artist',)
        model = Song


class EmailForm(forms.Form):
    name = forms.CharField()

    def __init__(self, instance=None, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)

        if instance is None:
            Email = get_email_class()
            self.instance = Email()
        else:
            self.instance = instance

        self.initial = model_to_dict(self.instance)

        for language_key, _ in LANGUAGES:
            field_name = 'html_{}'.format(language_key)
            self.fields[field_name] = forms.CharField(widget=forms.Textarea, required=False)
            self.fields[field_name].is_html = True

    def save(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        for field_name in cleaned_data.keys():
            setattr(self.instance, field_name, cleaned_data[field_name])

        self.instance.save()
        return self.instance
