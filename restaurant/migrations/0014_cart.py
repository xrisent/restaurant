# Generated by Django 4.2.6 on 2023-10-27 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_person_tg_id'),
        ('restaurant', '0013_remove_restaurant_photo_2_remove_restaurant_photo_3'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dishes', models.ManyToManyField(to='restaurant.dish')),
                ('drinks', models.ManyToManyField(to='restaurant.drink')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_auth.person')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
    ]