from rest_framework import serializers
from .models import Type, Dish, Restaurant, Table, Review


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    available_tables = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'

    def decrease_available_tables(self, obj):
        reserved_tables_count = obj.tables.filter(is_reserved=True).count()
        available_tables = obj.tables.count() - reserved_tables_count
        return available_tables
    
    def increase_available_tables(self, obj):
        not_reserved_tables_count = obj.tables.filter(is_reserved=False).count()
        available_tables = obj.tables.count() + not_reserved_tables_count
        return available_tables

    def get_rating(self, obj):
        positive_reviews = obj.review_set.filter(positive_or_not='positive').count()
        negative_reviews = obj.review_set.filter(positive_or_not='negative').count()
        return positive_reviews - negative_reviews


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'