from django.core.urlresolvers import resolve
from django.conf import settings


def current_view_name(request):
    return {'current_view_name': resolve(request.path_info).url_name}


def debug(_):
    return {'debug': settings.DEBUG}
