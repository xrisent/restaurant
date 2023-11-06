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

            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Сумма в центах
                currency='usd',
            )

            return Response({'client_secret': payment_intent.client_secret}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmPaymentView(APIView):
    def post(self, request, format=None):
        payment_intent_id = request.data.get('payment_intent_id')
        try:
            payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
            if payment_intent.status == 'succeeded':
                return Response({'message': 'Payment succeeded'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)