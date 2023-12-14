from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id','product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, required=False)
    order_number = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id','customer', 'order_date', 'address', 'order_item', 'order_number']

    def create(self, validated_data):
        order_item_data = validated_data.pop('order_item', [])

        last_order = Order.objects.order_by('-id').first()
        if last_order:
            last_order_number = int(last_order.order_number.split('ORD')[-1])
            new_order_number = f'ORD{last_order_number + 1:05}'
        else:
            new_order_number = 'ORD00001'

        validated_data['order_number'] = new_order_number
        instance = super(OrderSerializer, self).create(validated_data)

        for item_data in order_item_data:
            OrderItem.objects.create(order=instance, **item_data)

        return instance
