from django.urls import path
from . import views

urlpatterns = [
    # --------------------
    # Auth
    # --------------------
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('user/', views.current_user, name='current_user'),

    # --------------------
    # Vendor
    # --------------------
    path('vendor/create/', views.create_vendor, name='create_vendor'),

    # --------------------
    # Products
    # --------------------
    path('products/', views.product_list, name='product_list'),
    path('product/create/', views.create_product, name='create_product'),

    # --------------------
    # Cart
    # --------------------
    path('cart/add/', views.add_to_cart, name='add_to_cart'),

    # --------------------
    # Orders
    # --------------------
    path('order/create/', views.create_order, name='create_order'),

    # --------------------
    # Reviews
    # --------------------
    path('review/add/', views.add_review, name='add_review'),
]
