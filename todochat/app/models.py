from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


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
    image = models.ImageField(default='default.png', upload_to='server_pics')

    def __str__(self):
        return f'{self.name} server'
    
    def save(self, *args, **kwargs):
        super().save()
        self.users.add(self.owner)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('server_detail', kwargs={'pk': self.id})


class Channel(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)