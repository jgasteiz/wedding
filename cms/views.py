import csv
from datetime import datetime

from google.appengine.api import mail
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    RedirectView,
    UpdateView,
    View,
    FormView,
)

from wedding import mixins
from wedding.forms import EmailForm, InviteeForm
from wedding.models import Invitee, Song, get_email_class


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

    def get_context_data(self, **kwargs):
        ctx = super(InviteesView, self).get_context_data(**kwargs)
        Email = get_email_class()
        ctx['emails'] = Email.objects.all()
        return ctx

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


class SendEmailsView(View):
    def post(self, *args, **kwargs):

        invitee_ids = self.request.POST.getlist('invitees[]')
        email_id = self.request.POST.get('email')

        Email = get_email_class()

        for invitee_id in invitee_ids:
            invitee = Invitee.objects.get(pk=invitee_id)

            # Check if the email has already been sent to the invitee.
            emails_sent_to_invitee_ids = invitee.get_email_ids()
            if email_id in emails_sent_to_invitee_ids:
                continue

            email = Email.objects.get(pk=email_id)

            email_html = getattr(email, 'html_{}'.format(invitee.language))
            if email_html == '':
                email_html = """
                    Hey! You are invited to our wedding.
                    Check this out: https://magdaandjavi.appspot.com/en/
                    """

            message = mail.EmailMessage(
                sender="Javi Manzano <{}>".format(settings.EMAIL_FROM),
                subject="You're invited to our wedding"
            )

            message.to = "{} {} <{}>".format(invitee.first_name, invitee.last_name, invitee.email)
            message.html = email_html
            message.send()

            # Add email id to invitee emails list.
            if email_id not in emails_sent_to_invitee_ids:
                emails_sent_to_invitee_ids.append(email_id)
                invitee.emails = ','.join(emails_sent_to_invitee_ids)
                invitee.save()

        return HttpResponse('OK')

send_emails = SendEmailsView.as_view()


class EmailView(mixins.ViewNameMixin, ListView):
    model = None
    page_name = 'emails'
    template_name = 'cms/emails.html'

    def get_queryset(self):
        Email = get_email_class()
        return Email.objects.all()

emails = EmailView.as_view()


class EmailCreateView(mixins.ViewNameMixin, FormView):
    form_class = EmailForm
    page_name = 'emails'
    success_url = reverse_lazy('cms:emails')
    template_name = 'cms/email_form.html'

    def form_valid(self, form):
        form.save()
        return super(EmailCreateView, self).form_valid(form)

create_email = EmailCreateView.as_view()


class EmailUpdateView(mixins.ViewNameMixin, FormView):
    form_class = EmailForm
    page_name = 'emails'
    success_url = reverse_lazy('cms:emails')
    template_name = 'cms/email_form.html'

    def get(self, request, *args, **kwargs):
        Email = get_email_class()
        email_pk = self.kwargs.get('pk')
        self.object = Email.objects.get(pk=email_pk)
        return super(EmailUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        Email = get_email_class()
        email_pk = self.kwargs.get('pk')
        self.object = Email.objects.get(pk=email_pk)
        return super(EmailUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super(EmailUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EmailUpdateView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

update_email = EmailUpdateView.as_view()


class EmailDeleteView(mixins.ViewNameMixin, DeleteView):
    page_name = 'emails'
    success_url = reverse_lazy('cms:emails')
    template_name = 'cms/email_delete_confirmation.html'

    def get_object(self, queryset=None):
        Email = get_email_class()
        email_pk = self.kwargs.get('pk')
        return Email.objects.get(pk=email_pk)

delete_email = EmailDeleteView.as_view()


class EmailPreviewView(View):
    def get(self, *args, **kwargs):
        Email = get_email_class()
        email_pk = kwargs.get('pk')
        email = Email.objects.get(pk=email_pk)
        return HttpResponse(email.html_en)

preview_email = EmailPreviewView.as_view()
