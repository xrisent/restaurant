from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

urlpatterns = [
    path('create_payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('confirm_payment/', ConfirmPaymentView.as_view(), name='confirm-payment'),
    path('cancel_payment/', CancelPaymentView.as_view(), name='cancel-payment')
    # path('create_payment/', create_payment, name='create_payment'),
    # path('confirm_payment/', confirm_payment, name='confirm_payment'),
    # path('success/', payment_success, name='payment_success'),
]


urlpatterns += router.urls