from .models import Product, Subcategory, Category, Brand, CartItem


class ProductMixin:
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_user_context(self, **kwargs):
        context = kwargs
        context['cats'] = Category.objects.all()
        context['subcats'] = Subcategory.objects.all()
        context['brands'] = Brand.objects.all()
        if self.request.user.is_authenticated:
            context['cart'] = Product.objects.filter(cart_items__user=self.request.user, cart_items__is_ordered=False)
        return context


