from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProductViewSet, OrderViewSet,initialize_payment, verify_payment

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    # AUTH
    path("login/", views.login),
    path("register/", views.register),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("user/", views.current_user),

    # VENDOR
    path("vendor/create/", views.create_vendor),
    path("vendor/dashboard/", views.vendor_dashboard),

    # CART
    path("cart/add/", views.add_to_cart),

    # REVIEW
    path("review/add/", views.add_review),

    # ROUTER URLs
    path("", include(router.urls)),
    # initialize payment
    path('initialize/', initialize_payment),
     path('verify/<str:reference>/', verify_payment),

    
]
