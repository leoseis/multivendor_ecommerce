from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # AUTH
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/", views.current_user, name="current_user"),

    # VENDOR
    path("vendor/create/", views.create_vendor, name="create_vendor"),

    # PRODUCTS
    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.create_product, name="create_product"),

    # CART
    path("cart/add/", views.add_to_cart, name="add_to_cart"),

    # ORDER
    path("order/create/", views.create_order, name="create_order"),

    # REVIEW
    path("review/add/", views.add_review, name="add_review"),
    path("vendor/dashboard/", views.vendor_dashboard),

]
