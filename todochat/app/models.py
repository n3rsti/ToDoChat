from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.utils import timezone


class Server(models.Model):
    name = models.CharField(max_length=20)
    id = models.CharField(primary_key=True, default=name, max_length=18)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='ownership_servers',
    )
    users = models.ManyToManyField(
        User, 
        default=owner,  
    )
    image = models.ImageField(default='default.png', upload_to='server_pics', blank=True)

    def __str__(self):
        return f'{self.name} server'
    
    def save(self, *args, **kwargs):
        super().save()
        if self.channel_set.count() == 0:
            Channel.objects.create(server=self, name="main")
        self.users.add(self.owner)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('server_detail', kwargs={'pk': self.id})

class ServerInvitation(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="server_invitations")
    id = models.CharField(primary_key=True, max_length=10)
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_server_invitations", blank=True, null=True)

class Channel(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'Server: {self.server.name}, Channel: {self.name}'

    def get_absolute_url(self):
        return reverse('room', kwargs={'pk': self.server.id, 'room_name': self.name})

