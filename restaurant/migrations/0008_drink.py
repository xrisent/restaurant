# Generated by Django 4.2.6 on 2023-10-26 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_remove_dish_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Write here name of the drink', max_length=150)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='drinks/')),
                ('price', models.PositiveIntegerField(default=0, help_text='Write here price of the drink in som')),
                ('made_of', models.TextField(blank=True, help_text='Write here what is it made of', null=True)),
                ('type', models.CharField(choices=[('alcohol', 'Alcohol'), ('hot', 'Hot'), ('cold', 'Cold')], max_length=150)),
            ],
            options={
                'verbose_name': 'Drink',
                'verbose_name_plural': 'Drinks',
            },
        ),
    ]
