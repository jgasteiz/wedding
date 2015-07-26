from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^songs/$', views.songs, name='songs'),
    url(r'^songs/approve/$', views.approve_song, name='approve_song'),
    url(r'^songs/download/(?P<file_type>.*)/$', views.download_songs, name='download_songs'),
    url(r'^songs/update/(?P<pk>\d+)/$', views.update_song, name='update_song'),
    url(r'^songs/delete/(?P<pk>\d+)/$', views.delete_song, name='delete_song'),
    url(r'^rsvp/$', views.rsvp, name='rsvp'),
]

# handler403 = views.cms_forbidden
