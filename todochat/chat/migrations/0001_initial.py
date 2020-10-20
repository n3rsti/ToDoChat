# Generated by Django 3.0.7 on 2020-10-14 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_auto_20200213_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelMessage',
            fields=[
                ('id', models.CharField(default='error', max_length=18, primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Channel')),
            ],
        ),
    ]