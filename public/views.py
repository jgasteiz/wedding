from django.views.generic import TemplateView


class ViewNameMixin(object):
    page_name = None

    def get_context_data(self, **kwargs):
        ctx = super(ViewNameMixin, self).get_context_data(**kwargs)
        ctx['page_name'] = self.page_name
        return ctx


class HomeView(ViewNameMixin, TemplateView):
    page_name = 'home'
    template_name = 'public/home.html'

home = HomeView.as_view()


class WeddingDetailsView(ViewNameMixin, TemplateView):
    page_name = 'details'
    template_name = 'public/details.html'

details = WeddingDetailsView.as_view()


class SongWishlist(ViewNameMixin, TemplateView):
    page_name = 'song_wishlist'
    template_name = 'public/song-wishlist.html'

song_wishlist = SongWishlist.as_view()


class ContactView(ViewNameMixin, TemplateView):
    page_name = 'contact'
    template_name = 'public/contact.html'

contact = ContactView.as_view()
