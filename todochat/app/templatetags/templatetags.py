from django import template
from users.models import Profile
from itertools import chain

register = template.Library()

@register.filter
def get_first_num(value, arg):
    return value[:arg]


@register.filter
def shorter_name(value, length):
    return f'{value[:length]}...' if len(value) > length else value