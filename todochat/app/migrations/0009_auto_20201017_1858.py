# Generated by Django 3.0.7 on 2020-10-17 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200213_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
