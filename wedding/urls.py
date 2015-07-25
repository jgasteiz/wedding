from django.conf.urls import include, url

import session_csrf
session_csrf.monkeypatch()

urlpatterns = [
    url(r'^_ah/', include('djangae.urls')),
    url(r'^csp/', include('cspreports.urls')),
    url(r'^auth/', include('djangae.contrib.gauth.urls', namespace='login')),

    url(r'^cms/', include('cms.urls', namespace='cms')),
    url(r'', include('public.urls', namespace='public')),
]
