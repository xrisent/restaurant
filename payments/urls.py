from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreatePaymentView, ConfirmPaymentView

router = DefaultRouter()

urlpatterns = [
    path('create_payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('confirm_payment/', ConfirmPaymentView.as_view(), name='confirm-payment'),
]


urlpatterns += router.urls