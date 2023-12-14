from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
import datetime

# all customer list and customer create view
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# update an existing customer
class CustomerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# product list and product create view
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


#  Order create view
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        order_data = request.data
        order_item_data = order_data.pop('order_item', [])

        # Validate order cumulative weight
        total_weight = 0
        for item in order_item_data:
            product_id = item.get('product')
            quantity = item.get('quantity')
            product = Product.objects.get(pk=product_id)
            total_weight += product.weight * quantity

        if total_weight > 150:
            return Response({'detail': 'Order cumulative weight must be under 150kg'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate order date
        order_date = order_data.get('order_date')
        if order_date and order_date < str(datetime.date.today()):
            return Response({'detail': 'Order Date cannot be in the past'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, order_item_data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer, order_item_data):
        instance = serializer.save()

        # Create order items using OrderItemSerializer
        order_item_serializer = OrderItemSerializer(data=order_item_data, many=True)
        order_item_serializer.is_valid(raise_exception=True)
        order_item_serializer.save(order=instance)

        # Ensure transactions are committed
        instance.save()

# Order list view
class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Order Update view
class OrderUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# order list by product
class OrderListByProductView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        products = self.request.query_params.get('products', '').split(',')
        return Order.objects.filter(order_item__product__name__in=products)
    
# Order list by customer
class OrderListByCustomerView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        customer_name = self.request.query_params.get('customer', '')
        return Order.objects.filter(customer__name=customer_name)
