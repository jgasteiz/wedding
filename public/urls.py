from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^details/$', views.details, name='details'),
    url(r'^song-wishlist/$', views.song_wishlist, name='song_wishlist'),
    url(r'^rsvp/$', views.rsvp, name='rsvp'),
    url(r'^contact/$', views.contact, name='contact'),
]

# handler404 = views.public_not_found
