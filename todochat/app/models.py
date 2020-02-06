from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from PIL import Image
from django.conf import settings
from django.urls import reverse

class Server(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        default=owner, 
        related_name='server_users',
    )
    image = models.ImageField(default='default.png', upload_to='server_pics')

    def __str__(self):
        return f'{self.name} server'
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('server_detail', kwargs={'pk': self.name})

