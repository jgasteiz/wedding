from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'cms/home.html'

home = HomeView.as_view()
