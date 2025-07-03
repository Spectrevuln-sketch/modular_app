from django import template

register = template.Library()

@register.filter
def format_module_name(value):
    return value.replace('_', ' ').capitalize()
