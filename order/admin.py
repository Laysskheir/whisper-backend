from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_products_display', 'total_amount', 'order_status', 'order_date']

    def get_products_display(self, obj):
        # Assuming that 'products' is a ManyToManyField in your Order model
        products = obj.products.all()
        product_names = '/ '.join(str(product) for product in products)
        return product_names

    get_products_display.short_description = 'Products'
