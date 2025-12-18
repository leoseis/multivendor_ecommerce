from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vendor(request):
    store_name = request.data.get('store_name')
    description = request.data.get('description')

    if not store_name:
        return Response(
            {'error': 'Store name is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    vendor = Vendor.objects.create(
        user=request.user,
        store_name=store_name,
        description=description
    )

    request.user.is_vendor = True
    request.user.save()

    serializer = VendorSerializer(vendor)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    if not request.user.is_vendor:
        return Response(
            {'error': 'Only vendors can add products'},
            status=status.HTTP_403_FORBIDDEN
        )

    vendor = Vendor.objects.get(user=request.user)

    product = Product.objects.create(
        vendor=vendor,
        name=request.data.get('name'),
        slug=request.data.get('slug'),
        description=request.data.get('description'),
        price=request.data.get('price'),
        stock=request.data.get('stock'),
        category_id=request.data.get('category')
    )

    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(is_available=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))

    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += quantity
    cart_item.save()

    return Response({'message': 'Item added to cart'})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    if not items:
        return Response({'error': 'Cart is empty'})

    total = 0
    order = Order.objects.create(user=request.user, total_price=0)

    for item in items:
        OrderItem.objects.create(
            order=order,
            vendor=item.product.vendor,
            product=item.product,
            price=item.product.price,
            quantity=item.quantity
        )
        total += item.product.price * item.quantity

    order.total_price = total
    order.save()

    items.delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    Review.objects.create(
        user=request.user,
        product_id=request.data.get('product'),
        rating=request.data.get('rating'),
        comment=request.data.get('comment')
    )
    return Response({'message': 'Review added'})

# Create your views her