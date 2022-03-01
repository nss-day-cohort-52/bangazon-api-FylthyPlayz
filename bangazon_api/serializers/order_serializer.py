from rest_framework import serializers
from bangazon_api.models import Order
from bangazon_api.models.payment_type import PaymentType
from .payment_type_serializer import PaymentTypeSerializer

class OrderSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer()
    class Meta:
        model = Order
        fields = ('id', 'products', 'created_on', 'total', 'completed_on', 'payment_type')
        depth = 1

class UpdateOrderSerializer(serializers.ModelSerializer):
    paymentTypeId = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ('paymentTypeId', 'id')
