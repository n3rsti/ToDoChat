import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from app.models import Channel, Server
from channels.db import database_sync_to_async
from chat.models import ChannelMessage
from app.views import create_id
from django.contrib.auth.models import User

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
        return print(1)