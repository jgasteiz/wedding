

class ViewNameMixin(object):
    page_name = None

    def get_context_data(self, **kwargs):
        ctx = super(ViewNameMixin, self).get_context_data(**kwargs)
        ctx['page_name'] = self.page_name
        return ctx