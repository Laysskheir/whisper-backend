from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product-list'),
    path('product/<slug:slug>/', views.product_detail, name='product-detail'),
    path('collections/<slug:slug>/', views.collections, name='collections'),

]
