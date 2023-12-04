from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Slider, Category, ProductImages
from .serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404  

@api_view(["GET"])
def home(request):
    if request.method == "GET":
        products = Product.objects.filter(feature=True)
        product_serializer = ProductSerializer(products, many=True)

        sliders = Slider.objects.all()
        sliders_serializer = SliderSerializer(sliders, many=True)  

        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)

        brands = Brand.objects.all()
        brands_serializer = BrandSerializer(brands, many=True)
        
        data = {
            "products": product_serializer.data,
            "sliders": sliders_serializer.data,
            "categories": categories_serializer.data,
            "brands": brands_serializer.data,

        }

        return Response(data, status=status.HTTP_200_OK)  

@api_view(["GET"])
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all()
        colors = Color.objects.all()
        
        product_serializer = ProductSerializer(products, many=True)
        color_serializer = ColorSerializer(colors, many=True)

        data = {
            'products': product_serializer.data,
            'colors': color_serializer.data,
        }
         
        return Response(data, status=status.HTTP_200_OK)

@api_view(["GET"])
def collections(request, slug):
    if request.method == "GET":
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def product_detail(request, slug):
    if request.method == "GET":
        product = get_object_or_404(Product, slug=slug)
        related_products = Product.objects.all().exclude(slug=slug)

        serializer = ProductSerializer(product)
        related_serializer = ProductSerializer(related_products, many=True)

        return Response(
            {
                "product": serializer.data,
                "relatedProducts": related_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

