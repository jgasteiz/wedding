

class ViewNameMixin(object):
    page_name = None

    def get_context_data(self, **kwargs):
        ctx = super(ViewNameMixin, self).get_context_data(**kwargs)
        ctx['page_name'] = self.page_name
        return ctx


class OrderByMixin(object):
    def get_queryset(self):
        order_by = self.request.GET.get('order_by')
        if order_by:
            return self.model.objects.all().order_by(order_by)
        else:
            return self.model.objects.all()