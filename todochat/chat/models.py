from django.db import models
from app.models import Channel
from django.contrib.auth.models import User

# Create your models here.
class ChannelMessage(models.Model):
    id = models.CharField(primary_key=True, default="error", max_length=18)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)