from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, CartItem, Enquiry, BillingInfo
from .serializers import (
    ProductSerializer, CartItemSerializer,
    EnquirySerializer, BillingInfoSerializer,OrderSerializer
)

# 🎁 View Products
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# 🛒 Add to Cart
@api_view(['POST'])
def add_to_cart(request):
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# 📩 Send Enquiry
@api_view(['POST'])
def send_enquiry(request):
    serializer = EnquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# 🧾 Submit Billing Info
@api_view(['POST'])
def submit_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        return Response({"message": "Order placed successfully ✅"}, status=201)
    return Response(serializer.errors, status=400)

