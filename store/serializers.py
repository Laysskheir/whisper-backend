from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ["title", "description", "image"]


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)
    images = ProductImagesSerializer(many=True)
    brand = BrandSerializer()  # Nested serializer for brand
    category = CategorySerializer()  # Nested serializer for category

    class Meta:
        model = Product
        fields = "__all__"


# class ShippingAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ShippingAddress
#         fields = ['phone', 'firstName', 'lastName', 'country', 'streetAddress', 'city', 'state', 'postalCode']

# class OrderSerializer(serializers.ModelSerializer):
#     order_items = OrderItemSerializer(many=True, read_only=True)  # Use the correct serializer here

#     class Meta:
#         model = Order
#         fields = '__all__'

# class OrderSerializer(serializers.ModelSerializer):
#     orders = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Order
#         fields = '__all__'

#     def get_orders(self, obj):
#         items = obj.orderitem_set.all()
#         serializer = OrderSerializer(items, many=True)
#         return serializer.data


