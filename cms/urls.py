from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^songs/$', views.songs, name='songs'),
    url(r'^rsvp/$', views.rsvp, name='rsvp'),
]

# handler403 = views.cms_forbidden
