# Generated by Django 3.1.8 on 2021-04-16 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20210416_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userschat',
            name='id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
