# Generated by Django 4.2.6 on 2023-10-27 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0012_restaurant_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='photo_2',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='photo_3',
        ),
    ]
