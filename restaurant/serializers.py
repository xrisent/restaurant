from rest_framework import serializers
from .models import Type, Dish, Restaurant, Table, Review, Drink


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    available_tables = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'

    def get_available_tables(self, obj):
        return obj.get_available_tables()

    def get_rating(self, obj):
        return obj.rating


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'