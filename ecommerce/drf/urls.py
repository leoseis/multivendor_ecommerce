from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.current_user),
    path('vendor/create/', views.create_vendor),
    path('products/', views.product_list),
    path('product/create/', views.create_product),
    path('cart/add/', views.add_to_cart),
    path('order/create/', views.create_order),
    path('review/add/', views.add_review),
]
