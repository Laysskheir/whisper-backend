from django.urls import path
from .views import (
UserLoggedDataView,
SearchProductView
)

urlpatterns = [
    path('products-search/', SearchProductView.as_view(), name='products-search'),
    path('user-logged/', UserLoggedDataView.as_view(), name='users-logged'),
]