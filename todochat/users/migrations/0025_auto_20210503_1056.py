# Generated by Django 3.1.8 on 2021-05-03 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_usersmessage_target_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersmessage',
            name='target_users',
        ),
        migrations.AddField(
            model_name='usersmessage',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
