from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsVendor


from django.contrib.auth import get_user_model

from .models import (
    Vendor,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review,
)

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    VendorSerializer,
    ProductSerializer,
    OrderSerializer,
)

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
@api_view(["GET"])
def product_list(request):
    products = Product.objects.filter(is_available=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsVendor])
def create_product(request):

    vendor = Vendor.objects.get(user=request.user)

    product = Product.objects.create(
        vendor=vendor,
        name=request.data.get("name"),
        slug=request.data.get("slug"),
        description=request.data.get("description"),
        price=request.data.get("price"),
        stock=request.data.get("stock"),
        category_id=request.data.get("category"),
    )

    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


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
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    if not items.exists():
        return Response(
            {"error": "Cart is empty"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    total_price = 0
    order = Order.objects.create(user=request.user, total_price=0)

    for item in items:
        OrderItem.objects.create(
            order=order,
            vendor=item.product.vendor,
            product=item.product,
            price=item.product.price,
            quantity=item.quantity,
        )
        total_price += item.product.price * item.quantity

    order.total_price = total_price
    order.save()

    items.delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


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










    
