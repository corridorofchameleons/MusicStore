from django.contrib import admin
from .models import *


class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'slug']


class AdminSubcategory(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'order_n']


class ImageInline(admin.TabularInline):
    model = Image


class AdminProduct(admin.ModelAdmin):
    inlines = (ImageInline,)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product']


admin.site.register(SiteUser)
admin.site.register(Category, AdminCategory)
admin.site.register(Subcategory, AdminSubcategory)
admin.site.register(Product, AdminProduct)
admin.site.register(Brand)
admin.site.register(Review)
admin.site.register(Order1)
admin.site.register(CartItem, CartItemAdmin)
