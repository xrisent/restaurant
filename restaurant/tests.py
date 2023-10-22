from django.test import TestCase
from user_auth.models import Person
from .models import *

class TypeModelTest(TestCase):
    def test_type_str_representation(self):
        type = Type(type="Espanol")
        self.assertEqual(str(type), "Espanol")

class DishModelTest(TestCase):
    def test_dish_str_representation(self):
        type = Type(type="Espanol")
        dish = Dish(name="Meth", description="Best meth", type=type, price=10)
        self.assertEqual(str(dish), "Meth")

class RestaurantModelTest(TestCase):
    def test_available_tables(self):
        type = Type.objects.create(type="Espanol")
        restaurant = Restaurant.objects.create(name="Los Pollos Hermanos", type=type, average_bill=20, tables=10)
        Table.objects.create(restaurant=restaurant, number=1, is_reserved=False)
        Table.objects.create(restaurant=restaurant, number=2, is_reserved=True)
        self.assertEqual(restaurant.get_available_tables(), 9)

class ReviewModelTest(TestCase):
    def test_review_str_representation(self):
        type = Type.objects.create(type="Espanol")
        restaurant = Restaurant.objects.create(name="Los Pollos Hermanos", type=type, average_bill=20, tables=10)
        person = Person.objects.create(name="Rayan Gosling")
        review = Review.objects.create(restaurant=restaurant, person=person, content="Great food", positive_or_not="positive")
        self.assertEqual(str(review), "Rayan Gosling : positive")

class TableModelTest(TestCase):
    def test_table_str_representation(self):
        type = Type.objects.create(type="Espanol")
        restaurant = Restaurant.objects.create(name="Los Pollos Hermanos", type=type, average_bill=20, tables=10)
        table = Table.objects.create(restaurant=restaurant, number=1, is_reserved=False)
        self.assertEqual(str(table), "1 in Los Pollos Hermanos by None")
