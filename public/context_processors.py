from django.core.urlresolvers import resolve


def current_view_name(request):
    return {'current_view_name': resolve(request.path_info).url_name}
