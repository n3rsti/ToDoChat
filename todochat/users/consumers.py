import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from users.models import UsersChat, UsersMessage
from app.views import create_num_id
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'chat_{self.chat_id}'
        self.channel = UsersChat.objects.get(id=self.chat_id)
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
        while not UsersMessage.objects.filter(id=id).first() is None:
            id = create_num_id(20)
        return UsersMessage.objects.create(id=id, chat=channel, content=message, author=author_obj)


class ChatNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'chatnotifications_{self.chat_id}'
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
        channel_id = event['channel_id']
        # msg_id is used to prevent websocket connection from receiving messages multiple times from multiple tabs
        msg_id = event['msg_id']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'channel_id': channel_id,
            'msg_id': msg_id
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        channel_id = text_data_json['channel_id']
        msg_id = text_data_json['msg_id']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'notification',
                'channel_id': channel_id,
                'msg_id': msg_id
            }
        )
