from django.db import models
from user_auth.models import Person
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.http import JsonResponse


class Type(models.Model):
    type = models.CharField(max_length=150, help_text='Write here type of cuisine')

    def __str__(self) -> str:
        return f'{self.type}'
    
    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'


class Category(models.Model):
    category = models.CharField(max_length=150, help_text='Write here category of food')

    def __str__(self) -> str:
        return f'{self.category}'
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Dish(models.Model):
    name = models.CharField(max_length=150, help_text='Write here name of the dish')
    photo = models.ImageField(upload_to='dishes/', null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.PositiveIntegerField(default=0, help_text='Write here price of dish in som')
    made_of = models.TextField(help_text='Write here what is it made of', default='dk')
    amount = models.CharField(max_length=150, help_text='Write here amount of product', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'

    

class Drink(models.Model):

    CHOICES = [('alcohol', 'Alcohol'), ('hot', 'Hot'), ('cold', 'Cold')]

    name = models.CharField(max_length=150, help_text='Write here name of the drink')
    photo = models.ImageField(upload_to='drinks/', null=True, blank=True)
    price = models.PositiveIntegerField(default=0, help_text='Write here price of the drink in som')
    made_of = models.TextField(help_text='Write here what is it made of', null=True, blank=True)
    type = models.CharField(max_length=150, choices=CHOICES)
    amount = models.CharField(max_length=150, help_text='Write here amount of product', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Drink'
        verbose_name_plural = 'Drinks'


class Restaurant(models.Model):
    name = models.CharField(max_length=150, help_text='Write here name of the restaurant')
    description = models.TextField(help_text='Write here description of the restaurant', null=True, blank=True)
    photo_1 = models.ImageField(upload_to='restaurants/', null=True, blank=True)
    photo_2 = models.ImageField(upload_to='restaurants/', null=True, blank=True)
    type = models.ManyToManyField(Type)
    dishes = models.ManyToManyField(Dish)
    drinks = models.ManyToManyField(Drink)
    average_bill = models.IntegerField(default=0, help_text='Write here average bill of restaurant in som')
    tables = models.PositiveIntegerField(default=0, help_text='Write here amount of tables that can be reserved')
    address = models.CharField(max_length=150, null=True, blank=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    plan = models.ImageField(upload_to='plans/', null=True, blank=True)
    viewbox = models.CharField(max_length=150, null=True, blank=True, help_text='Need for plan')

    # Возвращает количество свободных столов
    def get_available_tables(self):
        reserved_tables_count = self.table_set.filter(is_reserved=True).count()
        available_tables = self.table_set.count() - reserved_tables_count
        return available_tables
    
    # Нужен для обновления рейтинга
    def update_rating(self):
        positive_reviews = self.review_set.filter(positive_or_not='positive').count()
        negative_reviews = self.review_set.filter(positive_or_not='negative').count()
        self.rating = positive_reviews - negative_reviews
        self.save()

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
    

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    is_reserved = models.BooleanField(default=False)
    reserved_by = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    reserved_time = models.DateTimeField(null=True, blank=True, help_text='Write here time when you will come')
    dishes = models.ManyToManyField(Dish)
    drinks = models.ManyToManyField(Drink)
    d = models.CharField(max_length=250, null=True, blank=True, help_text='Need for plan')

    def __str__(self) -> str:
        return f'{self.number} in {self.restaurant} by {self.reserved_by}'
    
    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'


class Cart(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish)
    drinks = models.ManyToManyField(Drink)
    total_price = models.PositiveIntegerField(default=0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.person}'
    
    # Высчитывание стоимости корзины
    def calculate_total_price(self):
        total_price = 0

        for dish in self.dishes.all():
            total_price += dish.price

        for drink in self.drinks.all():
            total_price += drink.price

        self.total_price = total_price
        self.save()
    
    # Добавление dish и drink к существующему
    def add_cart(self, dish, drink, restaurant):
        if dish is not None and dish not in self.dishes.all():
            if self.restaurant is None:
                self.restaurant_id = restaurant
                self.dishes.add(dish)
            elif int(restaurant) == int(self.restaurant_id):
                self.dishes.add(dish)

        if drink is not None and drink not in self.drinks.all():
            if self.restaurant is None:
                self.restaurant_id = restaurant
                self.drinks.add(drink)
            elif int(restaurant) == int(self.restaurant_id):
                self.drinks.add(drink)

        self.save()
        self.calculate_total_price()
        self.save()

    # Удаление объекта
    def remove_object_cart(self, dish, drink):

        dish_in_list = self.dishes.filter(pk=dish).exists()

        drink_in_list = self.drinks.filter(pk=drink).exists()

        if dish_in_list:
            self.dishes.remove(dish)

        if drink_in_list:
            self.drinks.remove(drink)

        self.calculate_total_price()
        self.save()

    # Очищение корзины
    def clear_cart(self):

        self.dishes.clear()
        self.drinks.clear()
        self.restaurant = None
        
        self.calculate_total_price()
        self.save()

    def transfer_cart(self, table_id):

        table = Table.objects.get(id=table_id)
        
        for dish in self.dishes.all():
            table.dishes.add(dish)
        for drink in self.drinks.all():
            table.drinks.add(drink)

        self.dishes.clear()
        self.drinks.clear()
        self.restaurant = None

        table.save()
        self.calculate_total_price()
        self.save()


    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class Review(models.Model):

    CHOICES = [('positive', 'Positive'), ('negative', 'Negative')]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='qwerty')
    content = models.TextField()
    person = models.ForeignKey(Person, on_delete=models.SET_DEFAULT, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    positive_or_not = models.CharField(max_length=100, choices=CHOICES, default='positive')

    def __str__(self) -> str:
        return f'{self.person} : {self.positive_or_not}'
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'



# Создает Tables, которое указано в ресторане, дабы мы могли дальше их забронировать
@receiver(post_save, sender=Restaurant)
def create_tables(sender, instance, created, **kwargs):
    if created:
        num_tables = instance.tables  
        for table_number in range(1, num_tables + 1):
            Table.objects.create(restaurant=instance, number=table_number)


# Создает Cart связанный с Person
@receiver(post_save, sender=Person)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(person=instance)


# Проверяет, чтобы Person не зарезервировал более 2 столов одного ресторана
@receiver(pre_save, sender=Table)
def check_table_reservation(sender, instance, **kwargs):
    if instance.reserved_by is not None:
        reservations_count = Table.objects.filter(restaurant=instance.restaurant, reserved_by=instance.reserved_by).count()
        if reservations_count >= 2:
            response_data = {'message': "Person can only reserve up to 2 tables in the same restaurant."}
            instance.is_reserved = False
            instance.reserved_by = None
            instance.reserved_time = None
            instance.dishes.clear()
            instance.drinks.clear()
            return JsonResponse(response_data, status=400)


@receiver(pre_save, sender=Table)
def pre_save_table(sender, instance, **kwargs):
    print(f"About to save table {instance.number}")