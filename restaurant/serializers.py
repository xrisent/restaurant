from rest_framework import serializers
from .models import Type, Table, Restaurant, Review, Dish, Drink, Cart, Category, CartItem

from user_auth.serializers import PersonSerializer


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class ReviewSerializerCreate(serializers.ModelSerializer): 
    class Meta:
        model = Review
        fields = '__all__'
        

class ReviewSerializerView(serializers.ModelSerializer):
    person = PersonSerializer() 

    class Meta:
        model = Review
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)
    drink = DrinkSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'dish', 'drink', 'quantity', 'total_price']


class CartSerializerCreate(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source='cartitem_set')

    class Meta:
        model = Cart
        fields = ['id', 'person', 'items', 'total_price']


class CartSerializerView(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source='cartitem_set')
    person = PersonSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'person', 'items', 'total_price']



class RestaurantSerializerCreate(serializers.ModelSerializer):
    available_tables = serializers.SerializerMethodField()
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

    def get_available_tables(self, obj):
        return obj.get_available_tables()
    

class DishSerializerView(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Dish
        fields = '__all__'



class RestaurantSerializerView(serializers.ModelSerializer):
    available_tables = serializers.SerializerMethodField()
    rating = serializers.FloatField(read_only=True)
    dishes = DishSerializerView(many=True, read_only=True)
    drinks = DrinkSerializer(many=True, read_only=True)
    type = TypeSerializer(many=True, read_only=True)
    reviews = ReviewSerializerView(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

    def get_available_tables(self, obj):
        return obj.get_available_tables()