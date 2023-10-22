from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def perform_create(self, serializer):
        serializer.increase_available_tables()
        serializer.decrease_available_tables()
        serializer.instance.update_rating()
        serializer.save()

    def perform_update(self, serializer):
        serializer.increase_available_tables()
        serializer.decrease_available_tables()
        serializer.instance.update_rating()
        serializer.save()


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAuthenticated]


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]