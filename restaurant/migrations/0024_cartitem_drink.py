# Generated by Django 4.2.6 on 2025-01-02 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0023_remove_cartitem_drink'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='drink',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.drink'),
        ),
    ]
