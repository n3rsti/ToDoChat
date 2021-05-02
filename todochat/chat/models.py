from django.db import models
from app.models import Channel
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class ChannelMessage(models.Model):
    id = models.CharField(primary_key=True, default="error", max_length=20)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    target_users = models.ManyToManyField(User, related_name="user_new_messages")
    # target_user is basically list of users who didn't read message

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(ChannelMessage, self).save(*args, **kwargs)
