from django.urls import path
from .views import *

urlpatterns = [
    path('vendor/create/', create_vendor),
    path('products/', product_list),
    path('products/create/', create_product),
    path('cart/add/', add_to_cart),
    path('order/create/', create_order),
    path('review/add/', add_review),
]
