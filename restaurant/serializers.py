from rest_framework import serializers
from .models import Type, Table, Restaurant, Review, Dish, Drink, Cart, Category

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


class CartSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartSerializerView(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)
    drinks = DrinkSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = '__all__'


class RestaurantSerializerCreate(serializers.ModelSerializer):
    available_tables = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'

    def get_available_tables(self, obj):
        return obj.get_available_tables()

    def get_rating(self, obj):
        return obj.rating
    

class DishSerializerView(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Dish
        fields = '__all__'



class RestaurantSerializerView(serializers.ModelSerializer):
  available_tables = serializers.SerializerMethodField()
  rating = serializers.SerializerMethodField()
  dishes = DishSerializerView(many=True, read_only=True)
  drinks = DrinkSerializer(many=True, read_only=True)
  type = TypeSerializer(many=True, read_only=True)
  reviews = serializers.SerializerMethodField()

  class Meta:
      model = Restaurant
      fields = '__all__'

  def __init__(self, *args, **kwargs):
      reviews = kwargs.pop('reviews', [])
      super(RestaurantSerializerView, self).__init__(*args, **kwargs)
      self.reviews_data = reviews

  def get_available_tables(self, obj):
      return obj.get_available_tables()

  def get_rating(self, obj):
      return obj.rating

  def get_reviews(self, obj):
      return ReviewSerializerView(self.reviews_data, many=True).data