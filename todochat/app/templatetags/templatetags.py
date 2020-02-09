from django import template

register = template.Library()

@register.filter
def get_first_num(value, arg):
    return value[:arg]
    
