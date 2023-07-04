from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404


class SiteUser(AbstractUser):
    patronym = models.CharField(max_length=30, blank=True, verbose_name='Patronym')
    address = models.CharField(max_length=50, blank=False, verbose_name='Address')
    phone = models.BigIntegerField(blank=True, null=True, verbose_name='Phone')

    class Meta(AbstractUser.Meta):
        pass


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='Category')
    slug = models.SlugField(verbose_name='slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Subcategory(models.Model):
    name = models.CharField(max_length=20, verbose_name='Subcategory')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='subcategories')
    slug = models.SlugField(verbose_name='slug')
    order_n = models.SmallIntegerField(verbose_name='Order', default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'


class Brand(models.Model):
    brand = models.CharField(max_length=20, verbose_name='Manufacturer')
    slug = models.SlugField(verbose_name='slug')

    def __str__(self):
        return self.brand


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    slug = models.SlugField(verbose_name='Slug', default=title)
    brand = models.ForeignKey(Brand, verbose_name='Brand', on_delete=models.PROTECT, related_name='products')
    subcategory = models.ForeignKey(Subcategory, verbose_name='Subcategory',
                                    on_delete=models.PROTECT, related_name='products')
    description = models.TextField(blank=True, verbose_name='Description')
    stock = models.PositiveIntegerField(verbose_name='Available')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    pic = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Review(models.Model):
    SCORES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.CharField(max_length=30)
    content = models.TextField()
    rating = models.SmallIntegerField(choices=SCORES)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f'Review on {self.product.title} {self.created_at.date()}'


class Order1(models.Model):
    order_number = models.IntegerField(unique=True, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price * item.qty for item in self.items.all()])

    def __str__(self):
        return f'Order {self.order_number}'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='cart_items')
    qty = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order1, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title
