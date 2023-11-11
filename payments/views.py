from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe
from decouple import config

from .serializers import PaymentSerializer

stripe.api_key = config('STRIPE_SECRET_KEY')

class CreatePaymentView(APIView):
    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            payment_method_id = serializer.validated_data['payment_method_id']

            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency='usd',
                payment_method=payment_method_id
            )

            return Response({'payment_intent_id': payment_intent.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmPaymentView(APIView):
    def post(self, request, format=None):
        payment_intent_id = request.data.get('payment_intent_id')
        try:
            payment_intent = stripe.PaymentIntent.confirm(payment_intent_id, return_url='http://127.0.0.1:8000/api/v1/payment/success/')
            if payment_intent.status == 'succeeded':
                return Response({'message': 'Payment succeeded'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class CancelPaymentView(APIView):
    def post(self, request, format=None):
        payment_intent_id = request.data.get('payment_intent_id')
        
        try:
            canceled_payment_intent = stripe.PaymentIntent.cancel(payment_intent_id)
            
            return Response({'message': 'Payment canceled'}, status=status.HTTP_200_OK)
        
        except stripe.error.StripeError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Payment
# from .forms import PaymentForm, ConfirmPaymentForm
# import stripe
# from decouple import config

# stripe.api_key = config('STRIPE_SECRET_KEY')

# @csrf_exempt
# def create_payment(request):
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']

#             # В этом примере предполагается, что вы получили идентификатор метода оплаты от клиента
#             payment_method_id = request.POST.get('payment_method_id')

#             # Создайте платеж в Stripe с указанным методом оплаты
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=int(amount * 100),  # Сумма в центах
#                 currency='usd',
#                 payment_method=payment_method_id,
#                 confirmation_method='manual',
#             )

#             # Сохраните payment_intent_id в базе данных
#             Payment.objects.create(payment_intent_id=payment_intent.id, amount=amount)

#             return JsonResponse({'payment_intent_id': payment_intent.id})

#     else:
#         form = PaymentForm()

#     return render(request, 'payment_form.html', {'form': form})

# @csrf_exempt
# def confirm_payment(request):
#     if request.method == 'POST':
#         form = ConfirmPaymentForm(request.POST)
#         if form.is_valid():
#             payment_intent_id = form.cleaned_data['payment_intent_id']

#             try:
#                 # Подтвердите платеж в Stripe с указанным return_url
#                 payment_intent = stripe.PaymentIntent.confirm(
#                     payment_intent_id,
#                     return_url='http://127.0.0.1:8000/api/v1/payment/success/',  # Замените на свой URL
#                 )

#                 if payment_intent.status == 'succeeded':
#                     # Обновите статус платежа в базе данных или выполните другие действия
#                     payment = Payment.objects.get(payment_intent_id=payment_intent_id)
#                     payment.status = 'succeeded'
#                     payment.save()

#                     return JsonResponse({'message': 'Payment succeeded'})

#                 else:
#                     return JsonResponse({'message': 'Payment failed'})

#             except stripe.error.StripeError as e:
#                 return JsonResponse({'error': str(e)})

#     return JsonResponse({'error': 'Invalid request method'})

# def payment_success(request):
#     return render(request, 'success.html')