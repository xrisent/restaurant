# Generated by Django 4.2.6 on 2023-10-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_dish_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='reserved_time',
            field=models.DateTimeField(blank=True, help_text='Write here time when you will come', null=True),
        ),
    ]
