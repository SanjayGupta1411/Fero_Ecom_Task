from django.urls import path
from .views import *

urlpatterns = [
    path('api/customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('api/customers/<int:pk>/', CustomerUpdateView.as_view(), name='customer-update'),
    path('api/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('api/orders/', OrderCreateView.as_view(), name='order-create'),
    path('api/orders/list', OrderListView.as_view(), name='order-list'),
    path('api/orders/update/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('api/orders/list-by-product/', OrderListByProductView.as_view(), name='order-list-by-product'),
    path('api/orders/list-by-customer/', OrderListByCustomerView.as_view(), name='order-list-by-customer'),
]