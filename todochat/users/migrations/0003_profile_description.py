# Generated by Django 3.0.2 on 2020-02-02 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200130_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
