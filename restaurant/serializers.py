from rest_framework import serializers
from .models import Type, Table, Restaurant, Review, Dish, Drink, Cart, Category, CartItem, Reservation, TableDish
from user_auth.models import Person

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
    restaurant_id = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = '__all__'

    def get_restaurant_id(self, obj):
        restaurant = obj.restaurant_set.first() 
        return restaurant.id if restaurant else None

class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = '__all__'




class TableDishSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), write_only=True)  # Add dish_id field
    drink = DrinkSerializer(read_only=True)

    class Meta:
        model = TableDish
        fields = ['id', 'reservation', 'dish', 'dish_id', 'drink', 'quantity', 'total_price']

class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ['id', 'number', 'restaurant', 'd', 'total_price']


class ReservationSerializer(serializers.ModelSerializer):
    table = TableSerializer(read_only=True)
    table_id = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), write_only=True)
    reserved_by = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    table_dishes = TableDishSerializer(many=True, write_only=True)  # allow write, but handle logic manually

    class Meta:
        model = Reservation
        fields = ['id', 'table', 'table_id', 'reserved_by', 'start_time', 'end_time', 'table_dishes']

    def validate(self, attrs):
        if 'table_id' not in attrs:
            raise serializers.ValidationError({'table_id': 'This field is required.'})
        return attrs

    def create(self, validated_data):
        table = validated_data.pop('table_id')  # Get the table object
        table_dishes_data = validated_data.pop('table_dishes', [])  # Get the table dishes data

        # Create the reservation
        reservation = Reservation.objects.create(table=table, **validated_data)

        # Create TableDish objects and associate them with the reservation
        for table_dish_data in table_dishes_data:
            dish = table_dish_data.get('dish_id')  # Use dish_id here
            quantity = table_dish_data.get('quantity')

            # Create the TableDish object with the dish and quantity
            TableDish.objects.create(
                reservation=reservation,
                dish=dish,  # Now assigning the actual Dish object
                quantity=quantity
            )

        return reservation

    # Optionally, you can override the `to_representation` method to include the table_dishes data in the response.
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        table_dishes = TableDish.objects.filter(reservation=instance)
        representation['table_dishes'] = TableDishSerializer(table_dishes, many=True).data
        return representation




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
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'
    

class DishSerializerView(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Dish
        fields = '__all__'



class RestaurantSerializerView(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)
    dishes = DishSerializerView(many=True, read_only=True)
    drinks = DrinkSerializer(many=True, read_only=True)
    type = TypeSerializer(many=True, read_only=True)
    reviews = ReviewSerializerView(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'