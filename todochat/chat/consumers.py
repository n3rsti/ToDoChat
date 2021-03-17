import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from app.models import Channel, Server
from chat.models import ChannelMessage
from app.views import create_num_id
from django.contrib.auth.models import User

"""
There are 2 websocket connections for each message for performance reasons. 

ChatConsumer is used to deliver messages
with all details: content, author, author image. ChatConsumer is used only in room.html for specific text channel
so message is not sent where it shouldn't be. 

ServerNotificationConsumer is used in all app_based and server_based (html base files) views so notification counter
can be updated everytime user gets message. It's only sending minimum required details: server_id, channel_id, msg_id.

Websocket connections are separate so they won't send unnecessary details every message.

"""


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.server_id = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_{self.server_id}_{self.room_name}'
        self.channel = Channel.objects.get(server=Server.objects.get(id=self.server_id), name=self.room_name)
        author = self.scope['user']
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author = text_data_json['author']
        image = text_data_json['image']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': author,
                'image': image
            }
        )
        async_to_sync(self.create_chat_message(message, author))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        author = event['author']
        image = event['image']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'image': image
        }))

    def create_chat_message(self, message, author):
        channel = self.channel
        id = create_num_id(20)
        author_obj = User.objects.get(username=author)
        while not ChannelMessage.objects.filter(id=id).first() is None:
            id = create_num_id(20)
        return ChannelMessage.objects.create(id=id, channel=channel, content=message, author=author_obj)


class ServerNotificationConsumer(ChatConsumer):
    def connect(self):
        self.server_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'server_{self.server_id}'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def notification(self, event):
        server_id = event['server']
        channel_id = event['channel']
        # msg_id is used to prevent websocket connection from receiving messages multiple times from multiple tabs
        msg_id = event['id']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'server': server_id,
            'channel': channel_id,
            'id': msg_id
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        server_id = text_data_json['server']
        channel_id = text_data_json['channel']
        # msg_id is used to prevent websocket connection from receiving messages multiple times from multiple tabs
        msg_id = text_data_json['id']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'notification',
                'server': server_id,
                'channel': channel_id,
                'id': msg_id
            }
        )
