# Generated by Django 3.1.8 on 2021-04-10 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20201019_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channelmessage',
            name='id',
            field=models.CharField(default='error', max_length=20, primary_key=True, serialize=False),
        ),
    ]