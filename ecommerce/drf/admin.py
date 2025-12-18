from django.contrib import admin
from .models import (
    User,
    Vendor,
    Category,
    Product,
    ProductImage,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
    Review
)

# =======================
# USERS & VENDORS
# =======================

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'is_vendor',
        'is_staff',
        'is_active'
    )
    list_filter = ('is_vendor', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('id',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'store_name',
        'user',
        'is_active',
        'created_at'
    )
    list_filter = ('is_active',)
    search_fields = ('store_name', 'user__email')


# =======================
# PRODUCTS
# =======================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'vendor',
        'category',
        'price',
        'stock',
        'is_available',
        'created_at'
    )
    list_filter = ('is_available', 'category', 'vendor')
    search_fields = ('name', 'vendor__store_name')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')


# =======================
# CART & ORDERS
# =======================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__email',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total_price',
        'status',
        'created_at'
    )
    list_filter = ('status',)
    search_fields = ('user__email',)
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'vendor',
        'product',
        'price',
        'quantity'
    )
    list_filter = ('vendor',)


# =======================
# PAYMENTS & REVIEWS
# =======================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'payment_method',
        'amount',
        'status',
        'paid_at'
    )
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_id',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product',
        'rating',
        'created_at'
    )
    list_filter = ('rating',)
    search_fields = ('user__email', 'product__name')
# Register your models here.
