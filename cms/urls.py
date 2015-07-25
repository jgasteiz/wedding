from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
]

# handler403 = views.cms_forbidden
