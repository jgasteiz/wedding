from django import template
register = template.Library()


@register.filter('add_css_class')
def add_css_class(field, class_name):
    return field.as_widget(attrs={'class': class_name})
