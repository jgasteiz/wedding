import csv
from datetime import datetime

import smtplib


from google.appengine.api import mail
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    RedirectView,
    DetailView,
    UpdateView,
    View,
)

from wedding import mixins
from wedding.forms import EmailCredentialsForm, InviteeForm
from wedding.models import EmailCredentials, Invitee, Song


class HomeView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("cms:songs")

home = HomeView.as_view()


class SongsView(mixins.OrderByMixin, mixins.ViewNameMixin, ListView):
    page_name = 'songs'
    template_name = 'cms/songs.html'
    model = Song

songs = SongsView.as_view()


class DownloadSongsView(View):
    def get(self, request, *args, **kwargs):
        file_type = kwargs.get('file_type')
        response = HttpResponse(content_type='text/{}'.format(file_type))

        approved_songs = Song.objects.filter(is_approved=True).order_by('artist')
        date_now = str(datetime.now())

        if file_type == 'csv':
            file_name = 'approved-songs-{}.csv'.format(date_now)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

            writer = csv.writer(response)
            writer.writerow(['Song title', 'Artist name', 'Submitted by'])

            for song in approved_songs:
                writer.writerow([
                    unicode(song.name).encode('utf-8'),
                    unicode(song.artist).encode('utf-8'),
                    unicode(song.submitted_by).encode('utf-8'),
                ])
        elif file_type == 'plain':
            file_name = 'approved-songs-{}.txt'.format(date_now)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
            for song in approved_songs:
                line = '{}, {}\n'.format(song.name, song.artist)
                response.write(unicode(line).encode('utf-8'))

        return response

download_songs = DownloadSongsView.as_view()


class UpdateSongView(mixins.ViewNameMixin, UpdateView):
    page_name = 'songs'
    template_name = 'cms/song_form.html'
    model = Song
    success_url = reverse_lazy('cms:songs')

update_song = UpdateSongView.as_view()


class DeleteSongView(mixins.ViewNameMixin, DeleteView):
    page_name = 'songs'
    template_name = 'cms/song_delete_confirmation.html'
    model = Song
    success_url = reverse_lazy('cms:songs')

delete_song = DeleteSongView.as_view()


class ApproveSong(View):
    success_url = reverse_lazy('cms:songs')

    def post(self, request, *args, **kwargs):
        song_id = int(request.POST.get('song_id'))
        song_approved = request.POST.get('is_approved') == 'True'
        song = Song.objects.get(id=song_id)
        song.is_approved = song_approved
        song.save()
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

approve_song = ApproveSong.as_view()


class InviteesView(mixins.OrderByMixin, mixins.ViewNameMixin, ListView):
    model = Invitee
    page_name = 'invitees'
    template_name = 'cms/invitees.html'

invitees = InviteesView.as_view()


class InviteeCreateView(mixins.ViewNameMixin, CreateView):
    form_class = InviteeForm
    model = Invitee
    page_name = 'invitees'
    success_url = reverse_lazy('cms:invitees')
    template_name = 'cms/invitee_form.html'

create_invitee = InviteeCreateView.as_view()


class InviteeUpdateView(mixins.ViewNameMixin, UpdateView):
    form_class = InviteeForm
    model = Invitee
    page_name = 'invitees'
    success_url = reverse_lazy('cms:invitees')
    template_name = 'cms/invitee_form.html'

update_invitee = InviteeUpdateView.as_view()


class InviteeDeleteView(mixins.ViewNameMixin, DeleteView):
    model = Invitee
    page_name = 'invitees'
    success_url = reverse_lazy('cms:invitees')
    template_name = 'cms/invitee_delete_confirmation.html'

delete_invitee = InviteeDeleteView.as_view()


class SendInvitationView(View):
    success_url = reverse_lazy('cms:invitees')

    def get(self, *args, **kwargs):
        invitee = Invitee.objects.get(pk=kwargs.get('pk'))
        credentials = EmailCredentials.get_instance()

        sender_address = "Javi Manzano <{}>".format(credentials.email_address)
        subject = "You're invited to our wedding"
        body = """Hey! You are invited to our wedding. Check this out: https://magdaandjavi.appspot.com/en/"""

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.ehlo()
        session.starttls()
        session.login(credentials.email_address, credentials.get_password())
        headers = "\r\n".join([
            "from: " + sender_address,
            "subject: " + subject,
            "to: " + invitee.email,
            "mime-version: 1.0",
            "content-type: text/html",
        ])

        content = headers + "\r\n\r\n" + body

        session.sendmail(credentials.email_address, invitee.email, content)

        # mail.send_mail(sender_address, invitee.email, subject, body)
        return redirect(self.success_url)

send_invitation = SendInvitationView.as_view()


class EmailCredentialsView(mixins.ViewNameMixin, DetailView):
    model = EmailCredentials
    page_name = 'email_credentials'
    template_name = 'cms/email_credentials_detail.html'

    def get_object(self, queryset=None):
        instance = self.model.get_instance()
        return instance

email_credentials = EmailCredentialsView.as_view()


class EmailCredentialsUpdateView(mixins.ViewNameMixin, UpdateView):
    form_class = EmailCredentialsForm
    model = EmailCredentials
    page_name = 'email_credentials'
    success_url = reverse_lazy('cms:email_credentials')
    template_name = 'cms/email_credentials_form.html'

    def get_object(self, queryset=None):
        instance = self.model.get_instance()
        return instance

email_credentials_update = EmailCredentialsUpdateView.as_view()
