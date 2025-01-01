from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *


class PersonSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Person
        fields = ['id', 'photo', 'name', 'email', 'number', 'tg_id', 'tg_code', 'user']
        read_only_fields = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'id', 'person', 'email', 'password', 'number'] 

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
        )
        user.set_password(validated_data['password'])
        user.save()

        number = validated_data['number']

        person = Person(user=user, name=user.username, number=number, email=user.email)
        person.save()

        return user
