from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from products.models import Product, CartItem, Order1, Subcategory, Category, Review, SiteUser
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import *


class ProductAPIList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SubcatAPIList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcat = self.kwargs['subcat_slug']
        return Product.objects.filter(subcategory=Subcategory.objects.get(slug=subcat))


class CatAPIList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcats = Subcategory.objects.filter(category=Category.objects.get(slug=self.kwargs['cat_slug']))
        return Product.objects.filter(subcategory__in=subcats)


class ProductAPIDetail(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer

    def get_object(self):
        return Product.objects.get(slug=self.kwargs['product_slug'])


class ListAPIReview(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        return Review.objects.filter(product=Product.objects.get(slug=self.kwargs['product_slug']))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, product=Product.objects.get(slug=self.kwargs['product_slug']))


class CartViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user, is_ordered=False)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = SiteUser.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class OrderAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order1.objects.filter(user=self.request.user)
