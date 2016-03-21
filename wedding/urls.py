from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

import session_csrf
session_csrf.monkeypatch()

from public import views as public_views


urlpatterns = [
    url(r'^_ah/', include('djangae.urls')),
    url(r'^csp/', include('cspreports.urls')),
    url(r'^auth/', include('djangae.contrib.gauth.urls', namespace='login')),
    url(r'^cms/', include('cms.urls', namespace='cms')),
]

public_patterns = [
    url(r'^$', public_views.home, name='home'),
    url(r'^details/$', public_views.details, name='details'),
    url(r'^agenda/$', public_views.agenda, name='agenda'),
    url(r'^song-wishlist/$', public_views.song_wishlist, name='song_wishlist'),
    url(r'^song-wishlist-thanks/$', public_views.song_wishlist_thanks, name='song_wishlist_thanks'),
    url(r'^rsvp/$', public_views.rsvp, name='rsvp'),
    url(r'^rsvp-thanks/$', public_views.rsvp_thanks, name='rsvp_thanks'),
    url(r'^contact/$', public_views.contact, name='contact'),
    url(r'^change_language/(?P<lang_code>.*)/$', public_views.change_language, name='change_language'),
]

urlpatterns += i18n_patterns(
    url(r'', include(public_patterns, namespace='public')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
