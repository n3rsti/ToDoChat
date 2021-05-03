from django import template
from users.models import UserInvitation
from app.models import Server, ServerInvitation

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
        return "inviting"  # I am inviting
    elif UserInvitation.objects.filter(invited=me, inviting=user).first() is not None:
        return "invited"  # I got invited
    else:
        return "no_invitation"


# Returns count of user's tasks in specific server
@register.filter
def get_user_task_count(user, server_id):
    return Server.objects.get(id=server_id).server_tasks.filter(assigned_for=user).count()


@register.filter
def get_server_invitation_status(user, server_id):
    server = Server.objects.get(id=server_id)
    return ServerInvitation.objects.filter(server=server, invited_user=user.user).first() is not None


@register.filter
def get_friends_chat_id(user):
    friends = user.profile.friends.all()
    users_chat = user.users_chat.all()
    chats = []
    notification_counter = []
    for friend in friends:
        chat = users_chat.filter(users=user).filter(users=friend).first()
        chats.append(chat)
        notification_counter.append(chat.usersmessage_set.filter(is_read=False).exclude(author=user).count())
    return zip(friends, chats, notification_counter)


@register.filter
def get_userschat_objects(request_user):
    chat_obj_list = []
    chat_objects = request_user.users_chat.all()
    friends = request_user.friends_set.all()
    for friend in friends:
        chat_obj_list.append(chat_objects.filter(users=request_user).filter(users=friend.user).first().id)
    return zip(friends, chat_obj_list)
