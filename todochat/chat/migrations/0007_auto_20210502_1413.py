# Generated by Django 3.1.8 on 2021-05-02 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_serverinvitation'),
        ('chat', '0006_auto_20210502_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channelmessage',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.channel'),
        ),
    ]