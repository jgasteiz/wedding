from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^songs/$', views.songs, name='songs'),
    url(r'^songs/approve/$', views.approve_song, name='approve_song'),
    url(r'^songs/download/(?P<file_type>.*)/$', views.download_songs, name='download_songs'),
    url(r'^songs/update/(?P<pk>\d+)/$', views.update_song, name='update_song'),
    url(r'^songs/delete/(?P<pk>\d+)/$', views.delete_song, name='delete_song'),

    url(r'^invitees/$', views.invitees, name='invitees'),
    url(r'^rsvp/create/$', views.create_invitee, name='invitee_create'),
    url(r'^rsvp/update/(?P<pk>\d+)/$', views.update_invitee, name='update_invitee'),
    url(r'^rsvp/delete/(?P<pk>\d+)/$', views.delete_invitee, name='delete_invitee'),
]

# handler403 = views.cms_forbidden
