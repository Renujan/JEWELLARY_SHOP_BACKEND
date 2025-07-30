from rest_framework import serializers
from .models import Product, CartItem, Enquiry, BillingInfo,Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'

class BillingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingInfo
        fields = ['full_name', 'address', 'city', 'phone_number', 'email']

class OrderSerializer(serializers.Serializer):
    billing_info = BillingInfoSerializer()
    cart_items = CartItemSerializer(many=True)

    def create(self, validated_data):
        billing_data = validated_data.pop('billing_info')
        cart_items_data = validated_data.pop('cart_items')

        billing = BillingInfo.objects.create(**billing_data)
        order = Order.objects.create(billing_info=billing)

        for item in cart_items_data:
            CartItem.objects.create(order=order, **item)

        return order
