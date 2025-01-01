from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.exceptions import PermissionDenied





from .models import *
from .serializers import *


class RestaurantViewSetView(viewsets.ModelViewSet):
  queryset = Restaurant.objects.all()
  serializer_class = RestaurantSerializerView
  permission_classes = [AllowAny]

  def retrieve(self, request, *args, **kwargs):
      instance = self.get_object()

      instance.update_rating()
      available_tables = instance.get_available_tables()

      reviews = Review.objects.filter(restaurant=instance)
      review_serializer = ReviewSerializerView(reviews, many=True)

      serializer = self.get_serializer(instance, reviews=reviews)

      serializer.data['available_tables'] = available_tables


      return Response(serializer.data)
    

class RestaurantViewSetCreate(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializerCreate
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.update_rating()
        available_tables = instance.get_available_tables()


        serializer = self.get_serializer(instance)
        serializer.data['available_tables'] = available_tables
        return Response(serializer.data)


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [AllowAny]


class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    permission_classes = [AllowAny]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerCreate
    permission_classes = [AllowAny]


class CartViewSetCreate(viewsets.ModelViewSet):
    serializer_class = CartSerializerCreate
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()  # Return an empty queryset for schema generation

        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this data.")

        queryset = Cart.objects.filter(person__user=user)

        for cart in queryset:
            cart.calculate_total_price()

        return queryset


class CartViewSetView(viewsets.ModelViewSet):
    serializer_class = CartSerializerView
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()  # Return an empty queryset for schema generation

        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("You must be logged in to view this data.")

        queryset = Cart.objects.filter(person__user=user)

        for cart in queryset:
            cart.calculate_total_price()

        return queryset
    


@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update':
            person_id = request.POST.get('person_id')
            dish_id = request.POST.get('dish_id')
            drink_id = request.POST.get('drink_id')
            restaurant_id = request.POST.get('restaurant_id')

            try:
                person = Person.objects.get(pk=person_id)
            except Person.DoesNotExist:
                return JsonResponse({'error': 'Person not found'}, status=404)

            cart, created = Cart.objects.get_or_create(person=person)
            
            cart.add_cart(dish=dish_id, drink=drink_id, restaurant=restaurant_id)

            return JsonResponse({'message': 'Cart updated successfully'})

        elif action == 'clear':

            person_id = request.POST.get('person_id')

            try:
                person = Person.objects.get(pk=person_id)
            except Person.DoesNotExist:
                return JsonResponse({'error': 'Person not found'}, status=404)

            cart, created = Cart.objects.get_or_create(person=person)

            cart.clear_cart()

            return JsonResponse({'message': 'Cart cleared successfully'})
        
        elif action == 'remove':

            person_id = request.POST.get('person_id')
            dish_id = request.POST.get('dish_id')
            drink_id = request.POST.get('drink_id')

            try:
                person = Person.objects.get(pk=person_id)
            except Person.DoesNotExist:
                return JsonResponse({'error': 'Person not found'}, status=404)
            
            cart = Cart.objects.get(person=person)

            cart.remove_object_cart(dish=dish_id, drink=drink_id)

            return JsonResponse({'message': 'Removed from cart successfully'})
        
        elif action == 'transfer':

            person_id = request.POST.get('person_id')
            table_id = request.POST.get('table_id')

            try:
                Table.objects.get(id=table_id)
            except Table.DoesNotExist:
                return JsonResponse({'error': 'Table not found'}, status=404)
            
            try:
                person = Person.objects.get(pk=person_id)
            except Person.DoesNotExist:
                return JsonResponse({'error': 'Person not found'}, status=404)
            
            cart = Cart.objects.get(person=person)

            cart.transfer_cart(table_id=table_id)

            return JsonResponse({'message': 'transfer made successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)