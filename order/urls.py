# from django.urls import path
# from .views import *

# urlpatterns = [
#     # path('orders/', ListOrdersView.as_view(), name='list_orders'),
#     # path('create_order/', CreateOrderView.as_view(), name='create_order'),
#      path('store-order/', StoreOrderView.as_view(), name='store_order'),
# ]


#/urls.py

from django.urls import path
from .views import StoreOrderView, CreateCheckoutSessionView, OrderView

urlpatterns = [
    path('orders/', OrderView.as_view(), name='create_order'),
    path('create_order/', StoreOrderView.as_view(), name='create_order'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
]
