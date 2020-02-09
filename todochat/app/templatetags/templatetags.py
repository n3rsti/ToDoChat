from django import template
from users.models import Profile
from itertools import chain

register = template.Library()

@register.filter
def get_first_num(value, arg):
    return value[:arg]


    