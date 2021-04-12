import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from users.models import UsersChat, UsersMessage, UserInvitation
from app.views import create_num_id, create_random_id
from django.contrib.auth.models import User
from app.models import ServerInvitation, Server


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'chat_{self.chat_id}'
        self.channel = UsersChat.objects.get(id=self.chat_id)
        self.user = User.objects.get(username=self.scope['user'])

        if self.user in self.channel.users.all():
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
        ws_type = text_data_json['type']
        author = text_data_json['author']
        image = text_data_json['image']
        if ws_type == "server_invitation":
            server_id = text_data_json['server_id']
            invited_user = text_data_json['invited_user']
            invitation_id = create_random_id(10)
            message = f'tdchat.net/i/{invitation_id}'
            async_to_sync(self.create_server_invitation(server_id, invited_user, invitation_id))
        else:
            message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': "chat_message",
                'message': message,
                'author': author,
                'image': image
            }
        )

        async_to_sync(self.create_chat_message(message))

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

    def create_chat_message(self, message):
        msg_id = create_num_id(20)
        author_obj = self.user
        while not UsersMessage.objects.filter(id=msg_id).first() is None:
            msg_id = create_num_id(20)
        return UsersMessage.objects.create(id=msg_id, chat=self.channel, content=message, author=author_obj)

    def create_server_invitation(self, server_id, invited_user, invitation_id):
        if ServerInvitation.objects.filter(id=invitation_id).first() is None:
            server = Server.objects.get(pk=server_id)
            invited = User.objects.get(username=invited_user)
            return ServerInvitation.objects.create(server=server, id=invitation_id, invited_user=invited)


class ChatNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'chatnotifications_{self.chat_id}'
        channel = UsersChat.objects.get(id=self.chat_id)
        user = self.scope['user']
        if user in channel.users.all():
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


class PersonalConsumer(WebsocketConsumer):
    def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = self.username
        self.user = self.scope['user']
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
        invitation_status = text_data_json['type']
        invited = text_data_json['invited']
        invited_img = text_data_json['invited_img']
        inviting = text_data_json['inviting']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': invitation_status,
                'invited': invited,
                'invited_img': invited_img,
                'inviting': inviting
            }
        )
        if self.user.username == inviting:
            if invitation_status == "invitation":
                async_to_sync(self.create_invitation(invited))
            elif invitation_status == "cancel_invitation":
                async_to_sync(self.delete_invitation(inviting, invited))

        elif self.user.username == invited:
            if invitation_status == "cancel_invitation":
                async_to_sync(self.delete_invitation(inviting, invited))
            elif invitation_status == "accept_invitation":
                async_to_sync(self.add_friend(inviting))

    def invitation(self, event):
        invited = event['invited']
        invited_img = event['invited_img']
        inviting = event['inviting']

        self.send(text_data=json.dumps({
            'type': 'invitation',
            'invited': invited,
            'invited_img': invited_img,
            'inviting': inviting
        }))

    def cancel_invitation(self, event):
        invited = event['invited']
        invited_img = event['invited_img']
        inviting = event['inviting']

        self.send(text_data=json.dumps({
            'type': 'cancel_invitation',
            'invited': invited,
            'invited_img': invited_img,
            'inviting': inviting
        }))

    def accept_invitation(self, event):
        invited = event['invited']
        invited_img = event['invited_img']
        inviting = event['inviting']

        """
        If users were friends before, UsersChat object is already created, so we can send its id and users can
        automatically connect to ws chat connection. Otherwise users will be connected after first refresh.
        """
        chat_obj = UsersChat.objects.filter(users=User.objects.get(username=invited)).filter(users=self.user).first()
        if chat_obj is not None:
            chat_obj = chat_obj.id

        self.send(text_data=json.dumps({
            'type': 'accept_invitation',
            'invited': invited,
            'invited_img': invited_img,
            'inviting': inviting,
            'chat': chat_obj
        }))

    def create_invitation(self, invited):
        invitation = UserInvitation.objects.filter(inviting=self.user, invited__username=invited).first()
        if invitation is None:
            invited_user = User.objects.get(username=invited)
            return UserInvitation.objects.create(inviting=self.user, invited=invited_user)

    def delete_invitation(self, inviting, invited):
        invitation = UserInvitation.objects.filter(inviting__username=inviting, invited__username=invited).first()
        if invitation is not None:
            return invitation.delete()

    def add_friend(self, inviting):
        invitation = UserInvitation.objects.filter(inviting__username=inviting, invited=self.user).first()
        inviting_user = User.objects.get(username=inviting)
        if (inviting_user not in self.user.friends_set.all()) and invitation is not None:
            return invitation.accept(inviting_user, self.user)
