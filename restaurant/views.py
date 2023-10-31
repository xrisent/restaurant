from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse





from .models import *
from .serializers import *


class RestaurantViewSetView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializerView
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.update_rating()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class RestaurantViewSetCreate(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializerCreate
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.update_rating()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated]


class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    permission_classes = [IsAuthenticated]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class CartViewSetCreate(viewsets.ModelViewSet):
    serializer_class = CartSerializerCreate
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(person__user=user)


        for cart in queryset:
            cart.calculate_total_price()

        return queryset

    

class CartViewSetView(viewsets.ModelViewSet):
    serializer_class = CartSerializerView
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
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

            try:
                person = Person.objects.get(pk=person_id)
            except Person.DoesNotExist:
                return JsonResponse({'error': 'Person not found'}, status=404)

            cart, created = Cart.objects.get_or_create(person=person)
            
            cart.add_cart(dish=dish_id, drink=drink_id)

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
            
            cart, created = Cart.objects.get_or_create(person=person)

            cart.remove_object_cart(dish=dish_id, drink=drink_id)

            return JsonResponse({'message': 'Removed from cart successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)