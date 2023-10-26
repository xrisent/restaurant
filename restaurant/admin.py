from django.contrib import admin
from .models import *

admin.site.register(Restaurant)
admin.site.register(Type)
admin.site.register(Dish)
admin.site.register(Review)
admin.site.register(Table)
admin.site.register(Drink)