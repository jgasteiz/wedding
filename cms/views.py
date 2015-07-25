from django.views.generic import TemplateView

from wedding import mixins


class HomeView(mixins.ViewNameMixin, TemplateView):
    page_name = 'home'
    template_name = 'cms/home.html'

home = HomeView.as_view()


class SongsView(mixins.ViewNameMixin, TemplateView):
    page_name = 'songs'
    template_name = 'cms/songs.html'

songs = SongsView.as_view()


class RsvpView(mixins.ViewNameMixin, TemplateView):
    page_name = 'rsvps'
    template_name = 'cms/rsvp.html'

rsvp = RsvpView.as_view()
