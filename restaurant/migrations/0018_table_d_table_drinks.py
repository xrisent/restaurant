# Generated by Django 4.2.6 on 2023-11-03 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0017_alter_cart_dishes_alter_cart_drinks'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='d',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='table',
            name='drinks',
            field=models.ManyToManyField(to='restaurant.drink'),
        ),
    ]