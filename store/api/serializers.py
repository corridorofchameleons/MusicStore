from rest_framework import serializers
from products.models import Product, CartItem, Review, SiteUser, Order1


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ['product', 'author', 'content', 'rating', 'created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    review_set = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = ['pk', 'title', 'brand', 'subcategory', 'price', 'review_set']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'title', 'brand', 'subcategory', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CartItem
        exclude = ('order', 'is_ordered')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SiteUser
        fields = ['username', 'first_name', 'patronym', 'last_name', 'email', 'address', 'phone']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ['is_ordered']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order1
        exclude = ['confirmed']
