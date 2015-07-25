from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, FormView
from datetime import date

from wedding import mixins
from wedding.forms import SongForm


class HomeView(mixins.ViewNameMixin, TemplateView):
    page_name = 'home'
    template_name = 'public/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        delta = date(2016, 6, 25) - date.today()
        ctx['days_until_wedding'] = delta.days
        return ctx

home = HomeView.as_view()


class WeddingDetailsView(mixins.ViewNameMixin, TemplateView):
    page_name = 'details'
    template_name = 'public/details.html'

details = WeddingDetailsView.as_view()


class SongWishlistView(mixins.ViewNameMixin, FormView):
    page_name = 'song_wishlist'
    template_name = 'public/song-wishlist.html'
    form_class = SongForm
    success_url = reverse_lazy('public:song_wishlist_thanks')

    def form_valid(self, form):
        form.save()
        return super(SongWishlistView, self).form_valid(form)

song_wishlist = SongWishlistView.as_view()


class SongSubmissionThanks(mixins.ViewNameMixin, TemplateView):
    page_name = 'song_wishlist'
    template_name = 'public/song-wishlist-thanks.html'

song_wishlist_thanks = SongSubmissionThanks.as_view()


class RSVPView(mixins.ViewNameMixin, TemplateView):
    page_name = 'rsvp'
    template_name = 'public/rsvp.html'

rsvp = RSVPView.as_view()


class ContactView(mixins.ViewNameMixin, TemplateView):
    page_name = 'contact'
    template_name = 'public/contact.html'

contact = ContactView.as_view()
