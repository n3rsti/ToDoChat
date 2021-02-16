from django import template
register = template.Library()
from chat.models import Channel, ChannelMessage
from app.models import Server, ServerInvitation
from users.models import UsersChat, UsersMessage
from django.urls import reverse
import re


def url_target_blank(text):
    reg = "^(.*(http:\/\/todochat.com\/i\/)([a-zA-Z0-9]{10}).*)$"
    reg_match = re.findall(reg, text)
    if len(reg_match) > 0:
        inv_id = reg_match[0][2]
        print(inv_id)
        invitation = ServerInvitation.objects.filter(id=inv_id).first()
        if invitation:
            text = text.replace(reg_match[0][1]+reg_match[0][2], invitation.get_absolute_url())
            return text
    return text.replace('<a ', '<a target="_blank" ')

url_target_blank = register.filter(url_target_blank, is_safe=True)

@register.filter
def author_filter(id, index):
    if index == 1:
        return False
    channel = Channel.objects.get(id=id)
    messages = ChannelMessage.objects.filter(channel=channel).order_by('created')
    if messages.count() > 50:
        messages = messages[messages.count() - 50:messages.count()]
    message = messages[index - 1]
    previous = messages[index - 2]
    if message.author == previous.author:
        return True
    else:
        return False

@register.filter
def chat_author_filter(id, index):
    if index == 1:
        return False
    channel = UsersChat.objects.get(id=id)
    messages = UsersMessage.objects.filter(chat=channel).order_by('created')
    if messages.count() > 50:
        messages = messages[messages.count() - 50:messages.count()]
    message = messages[index-1]
    previous = messages[index-2]
    if message.author == previous.author:
        return True
    else:
        return False

@register.filter
def get_last_messages(messages, quantity):
    if messages.count() < quantity:
        return messages
    messages = messages[messages.count() - quantity:messages.count()]
    return messages

