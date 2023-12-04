#serialzers.py
from rest_framework import serializers
from store.serializers import ProductSerializer
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
