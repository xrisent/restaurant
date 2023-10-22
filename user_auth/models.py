from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    # Пользователь
    name = models.CharField(max_length=150, help_text='Write here name of person')
    photo = models.ImageField(upload_to='persons/', null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True, help_text='Write here email of person')
    number = models.CharField(max_length=30, null=True, blank=True, help_text='Write here number of person')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.name}'
    
    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
