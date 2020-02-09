from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.cache import cache 
import datetime
from todochat import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    description = models.CharField(max_length=100, default='')
    is_online = models.BooleanField(default=False)
    friends = models.ManyToManyField(User, related_name='friends')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    