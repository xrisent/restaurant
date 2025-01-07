from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.decorators import action



from .models import *
from .serializers import *


class RestaurantViewSetView(viewsets.ModelViewSet):
  queryset = Restaurant.objects.all()
  serializer_class = RestaurantSerializerView
  permission_classes = [AllowAny]

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()

    instance.update_rating()

    reviews = Review.objects.filter(restaurant=instance)
    review_serializer = ReviewSerializerView(reviews, many=True)

    serializer = self.get_serializer(instance)

    # Optionally include reviews if needed, but it's already part of the serializer
    serializer.data['reviews'] = review_serializer.data

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

    @action(detail=True, methods=['post'], url_path='reserve')
    def reserve_table(self, request, pk=None):
        """
        Reserve a table for a given time period.
        """
        table = self.get_object()
        start_time = request.data.get("start_time")
        duration_hours = request.data.get("duration_hours")
        person_id = request.data.get("person_id")

        if not start_time or not duration_hours or not person_id:
            raise ValidationError("start_time, duration_hours, and person_id are required.")

        start_time = datetime.fromisoformat(start_time)  # Преобразуем строку в datetime
        duration_hours = int(duration_hours)

        person = Person.objects.get(id=person_id)

        # Проверка на пересечение времени
        end_time = start_time + timedelta(hours=duration_hours)
        reservation = Reservation(
            table=table,
            reserved_by=person,
            start_time=start_time,
            end_time=end_time
        )

        if reservation.is_overlapping():
            raise ValidationError("The table is already reserved for this time range.")

        reservation.save()

        for table in Table.objects.all():
            table.calculate_total_price()

        return Response({"message": "Table reserved successfully!", "reservation": ReservationSerializer(reservation).data})



class TableDishView(viewsets.ModelViewSet):
    queryset = TableDish.objects.all()
    serializer_class = TableDishSerializer
    permission_classes = [IsAuthenticated]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerCreate
    permission_classes = [AllowAny]


class CartItemView(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]


class CartViewSetCreate(viewsets.ModelViewSet):
    serializer_class = CartSerializerCreate
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()  # For schema generation

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
            return Cart.objects.none()  # For schema generation

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
            quantity = int(request.POST.get('quantity', 1))
            restaurant_id = request.POST.get('restaurant_id')

            try:
                person = Person.objects.get(pk=person_id)
            except Person.DoesNotExist:
                return JsonResponse({'error': 'Person not found'}, status=404)

            cart, created = Cart.objects.get_or_create(person=person)

            cart.add_cart(dish_id=dish_id, drink_id=drink_id, restaurant_id=restaurant_id, quantity=quantity)

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
            quantity = int(request.POST.get('quantity', 1))

            try:
                person = Person.objects.get(pk=person_id)
            except Person.DoesNotExist:
                return JsonResponse({'error': 'Person not found'}, status=404)

            cart = Cart.objects.get(person=person)

            cart.remove_from_cart(dish_id=dish_id, drink_id=drink_id, quantity=quantity)

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

            return JsonResponse({'message': 'Transfer made successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)