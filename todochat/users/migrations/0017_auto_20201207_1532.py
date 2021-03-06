# Generated by Django 3.0.7 on 2020-12-07 15:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0016_auto_20201203_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='background',
            field=models.ImageField(blank=True, default='default_background.jpg', upload_to='background_images'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
