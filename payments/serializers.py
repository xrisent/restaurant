from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method_id = serializers.CharField()

# ('pm_card_visa', 'Visa (тестовая)'),
# ('pm_card_mastercard', 'MasterCard (тестовая)'),