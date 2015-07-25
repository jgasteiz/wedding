from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import (
    TemplateView,
    UpdateView,
    DeleteView,
    View,
    ListView,
)

from wedding import mixins
from wedding.models import Song


class HomeView(mixins.ViewNameMixin, TemplateView):
    page_name = 'home'
    template_name = 'cms/home.html'

home = HomeView.as_view()


class SongsView(mixins.ViewNameMixin, ListView):
    page_name = 'songs'
    template_name = 'cms/songs.html'
    model = Song

songs = SongsView.as_view()


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


class RsvpView(mixins.ViewNameMixin, TemplateView):
    page_name = 'rsvps'
    template_name = 'cms/rsvp.html'

rsvp = RsvpView.as_view()
