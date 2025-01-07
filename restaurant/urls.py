from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'type', views.TypeViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'dish', views.DishViewSet)
router.register(r'drink', views.DrinkViewSet)
router.register(r'restaurant_view', views.RestaurantViewSetView)
router.register(r'restaurant_create', views.RestaurantViewSetCreate)
router.register(r'table', views.TableViewSet)
router.register(r'table_dishes', views.TableDishView)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'review', views.ReviewViewSet)
router.register(r'cart_view', views.CartViewSetView, basename='cart_view')
router.register(r'cart_create', views.CartViewSetCreate, basename='cart_create')
router.register(r'cart_items', views.CartItemView)


urlpatterns = [
    path('', include(router.urls)),
    path('cart_update/', views.update_cart, name='cart-update')
]