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
    url(r'^invitees/create/$', views.create_invitee, name='invitee_create'),
    url(r'^invitees/update/(?P<pk>\d+)/$', views.update_invitee, name='update_invitee'),
    url(r'^invitees/delete/(?P<pk>\d+)/$', views.delete_invitee, name='delete_invitee'),

    url(r'^invitation-emails/$', views.invitation_email, name='invitation_emails'),
    url(r'^invittaion-emails/create/$', views.invitation_email_create, name='invitation_email_create'),
    url(r'^invitation-emails/update/$', views.invitation_email_update, name='invitation_email_update'),

    url(r'^send-invitation/(?P<pk>\d+)/$', views.send_invitation, name='send_invitation'),
]

# handler403 = views.cms_forbidden
