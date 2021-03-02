from django import template
from users.models import User, UserInvitation
from app.models import Server

register = template.Library()


@register.filter
def get_first_num(value, arg):
    return value[:arg]


@register.filter
def shorter_name(value, length):
    return f'{value[:length]}...' if len(value) > length else value


@register.filter
def get_invitation_status(user, me):
    if UserInvitation.objects.filter(invited=user, inviting=me).first() is not None:
        return "inviting" # I am inviting
    elif UserInvitation.objects.filter(invited=me, inviting=user).first() is not None:
        return "invited" # I got invited
    else:
        return "no_invitation"


# Returns count of user's tasks in specific server
@register.filter
def get_user_task_count(user, server_id):
    return Server.objects.get(id=server_id).server_tasks.filter(assigned_for=user).count();

