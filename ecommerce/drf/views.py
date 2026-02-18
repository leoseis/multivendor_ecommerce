from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Vendor, Product, Cart, CartItem, Order, OrderItem, Review
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    VendorSerializer,
    ProductSerializer,
    OrderSerializer,
)
from .permissions import IsVendor  # make sure this exists

User = get_user_model()




# login
@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "is_vendor": getattr(user, "is_vendor", False),
        }
    })


# =========================
# AUTH
# =========================
@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )







@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# =========================
# VENDOR
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_vendor(request):

    if request.user.is_vendor:
        return Response(
            {"error": "You are already a vendor."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    store_name = request.data.get("store_name")
    description = request.data.get("description", "")

    if not store_name:
        return Response(
            {"error": "Store name is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    vendor = Vendor.objects.create(
        user=request.user,
        store_name=store_name,
        description=description,
    )

    request.user.is_vendor = True
    request.user.save()

    serializer = VendorSerializer(vendor)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# =========================
# PRODUCTS
# =========================
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if not self.request.user.is_vendor:
            raise PermissionDenied("Only vendors can create products.")

        vendor = Vendor.objects.get(user=self.request.user)
        serializer.save(vendor=vendor)




# =========================
# CART
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )

    if not created:
        cart_item.quantity += quantity

    cart_item.save()

    return Response({"message": "Item added to cart"})


# =========================
# ORDER
# =========================



# =========================
# REVIEW
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request):
    Review.objects.create(
        user=request.user,
        product_id=request.data.get("product"),
        rating=request.data.get("rating"),
        comment=request.data.get("comment"),
    )

    return Response(
        {"message": "Review added successfully"},
        status=status.HTTP_201_CREATED,
    )



@api_view(["GET"])
@permission_classes([IsAuthenticated, IsVendor])
def vendor_dashboard(request):

    vendor = Vendor.objects.get(user=request.user)

    products = Product.objects.filter(vendor=vendor)
    orders = OrderItem.objects.filter(vendor=vendor)

    total_revenue = sum(
        item.price * item.quantity for item in orders
    )

    return Response({
        "store_name": vendor.store_name,
        "total_products": products.count(),
        "total_orders": orders.count(),
        "total_revenue": total_revenue,
    })




class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Buyer → their orders
        if not user.is_vendor:
            return Order.objects.filter(user=user)

        # Vendor → orders with their products
        return Order.objects.filter(
            orderitem__vendor__user=user
        ).distinct()


    @action(detail=False, methods=["post"])
    def create_order(self, request):
        user = request.user

        try:
            cart = user.cart
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=400)

        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        with transaction.atomic():
            total_price = 0

            # 🔥 Validate items
            for item in cart_items:
                product = item.product

                # ❌ Vendor cannot buy own product
                if user.is_vendor and product.vendor.user == user:
                    return Response({
                        "error": f"You cannot order your own product: {product.name}"
                    }, status=400)

                # ❌ Not available
                if not product.is_available:
                    return Response({
                        "error": f"{product.name} is not available"
                    }, status=400)

                # ❌ Stock check
                if product.stock < item.quantity:
                    return Response({
                        "error": f"Not enough stock for {product.name}"
                    }, status=400)

                total_price += product.price * item.quantity

            # 🔥 Create Order
            order = Order.objects.create(
                user=user,
                total_price=total_price
            )

            # 🔥 Create OrderItems + reduce stock
            order_items = []

            for item in cart_items:
                product = item.product

                product.stock -= item.quantity
                product.save()

                order_items.append(OrderItem(
                    order=order,
                    vendor=product.vendor,
                    product=product,
                    price=product.price,
                    quantity=item.quantity
                ))

            OrderItem.objects.bulk_create(order_items)

            # 🔥 Clear cart
            cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        order = self.get_object()
        user = request.user

        # ❌ Only vendors
        if not user.is_vendor:
            return Response({"error": "Only vendors can update order"}, status=403)

        # ❌ Not their order
        if not order.orderitem_set.filter(vendor__user=user).exists():
            return Response({"error": "Not your order"}, status=403)

        status_value = request.data.get("status")

        valid_status = [choice[0] for choice in Order.STATUS_CHOICES]

        if status_value not in valid_status:
            return Response({"error": "Invalid status"}, status=400)

        order.status = status_value
        order.save()

        return Response({"message": "Order status updated"})








    
