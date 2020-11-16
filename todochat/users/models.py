from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    background = models.ImageField(default='default_background.jpg', upload_to='background_images')
    description = models.CharField(max_length=100, default='')
    is_online = models.BooleanField(default=False)
    friends = models.ManyToManyField(User, related_name='friends_set')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        background = Image.open(self.background.path)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class UserInvitation(models.Model):
    inviting = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inviting_set')
    invited = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited_user')


class UsersChat(models.Model):
    users = models.ManyToManyField(User, related_name="users_chat")

class UsersMessage(models.Model):
    id = models.CharField(primary_key=True, default="error", max_length=100)
    chat = models.ForeignKey(UsersChat, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created     = models.DateTimeField(editable=False, default=timezone.now)
    modified    = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(ChannelMessage, self).save(*args, **kwargs)