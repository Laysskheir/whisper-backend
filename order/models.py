# models.py
from django.db import models
from user.models import User
from store.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
