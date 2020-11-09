from django import template
register = template.Library()
from chat.models import Channel, ChannelMessage
from app.models import Server



def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')

url_target_blank = register.filter(url_target_blank, is_safe=True)

def author_filter(id, index):
    if index == 1:
        return False
    channel = Channel.objects.get(id=id)
    messages = ChannelMessage.objects.filter(channel=channel).order_by('created')
    message = messages[index-1]
    previous = messages[index-2]
    if message.author == previous.author:
        return True
    else:
        return False
    

author_filter = register.filter(author_filter)