import time
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView, CreateView, DeleteView, ListView

from .filters import ProductFilter
from .forms import ChangeUserInfoForm, RegisterUserForm, ReviewForm, CartForm
from .models import SiteUser, Product, Subcategory, Category, Brand, Review, Order1, CartItem
from .utils import ProductMixin

SITE_TITLE = 'RandomName Store :: '

menu_context = {
    'brands': Brand.objects.all(),
    'subcats': Subcategory.objects.all(),
    'cats': Category.objects.all(),
}


class RegisterUser(ProductMixin, CreateView):
    model = SiteUser
    template_name = 'register_user.html'
    form_class = RegisterUserForm
    extra_context = {'title': SITE_TITLE + 'Register'}
    success_url = reverse_lazy('profile')


class PLoginView(ProductMixin, LoginView):
    template_name = 'login.html'
    extra_context = {'title': SITE_TITLE + 'Login'} | menu_context


class PLogoutView(ProductMixin, LoginRequiredMixin, LogoutView):
    pass


class ChangeUserInfo(ProductMixin, LoginRequiredMixin, UpdateView):
    model = SiteUser
    template_name = 'change_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    extra_context = {'title': SITE_TITLE + 'User Data'} | menu_context

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ChangePassword(ProductMixin, LoginRequiredMixin, PasswordChangeView):
    model = SiteUser
    template_name = 'change_password.html'
    success_url = reverse_lazy('profile')
    extra_context = {'title': SITE_TITLE + 'Password Change'} | menu_context


@login_required()
def profile(request):
    context = {'title': SITE_TITLE + 'Profile'} | menu_context
    return render(request, 'profile.html', context)


class DeleteUser(ProductMixin, LoginRequiredMixin, DeleteView):
    model = SiteUser
    template_name = 'delete_user.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': SITE_TITLE + 'Kill myself'} | menu_context

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class HomeView(ProductMixin, ListView):

    def get_queryset(self):
        queryset = Product.objects.all()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = self.filterset.form
        c_def = self.get_user_context(title=SITE_TITLE + 'Home')
        return context | c_def


class SubcatView(ProductMixin, ListView):

    def get_queryset(self):
        queryset = Product.objects.filter(subcategory=Subcategory.objects.get(slug=self.kwargs['subcat_slug']))
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = self.filterset.form
        c_def = self.get_user_context(title=SITE_TITLE + Subcategory.objects.get(slug=self.kwargs['subcat_slug']).name)
        return context | c_def


class CatView(ProductMixin, ListView):

    def get_queryset(self):
        subcats = Subcategory.objects.filter(category=Category.objects.get(slug=self.kwargs['cat_slug']))
        queryset = Product.objects.select_related('subcategory').filter(subcategory__in=subcats)
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = self.filterset.form
        c_def = self.get_user_context(title=SITE_TITLE + Category.objects.get(slug=self.kwargs['cat_slug']).name)
        return context | c_def


class SearchView(ProductMixin, ListView):

    def get_queryset(self):
        queryset = Product.objects.filter(title__icontains=self.request.GET.get('req', ''))
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filter'] = self.filterset.form
        context['initial'] = self.request.GET.get('req')
        c_def = self.get_user_context(title=SITE_TITLE + 'Search')
        return context | c_def


def product_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    images = product.image_set.all()
    reviews = product.review_set.all()

    def get_avg_rating():
        if reviews.count():
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            return f'{avg_rating:.1f}'
        else:
            return None

    def in_cart():
        return CartItem.objects.filter(user=request.user, is_ordered=False, product=product).exists()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.cleaned_data['product'] = Product.objects.get(slug=product_slug)
            form.cleaned_data['author'] = request.user.username
            try:
                Review.objects.create(**form.cleaned_data)
            except:
                form.add_error(None, 'Error adding a review')
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'form': form,
        'title': SITE_TITLE + Product.objects.get(slug=product_slug).title,
        'avg_rating': get_avg_rating(),
    }

    if request.user.is_authenticated:
        context['in_cart'] = in_cart()

    return render(request, 'product_view.html', context | menu_context)


@require_POST
def cart_add(request, prod_pk):
    CartItem.objects.get_or_create(product=Product.objects.get(pk=prod_pk), user=request.user, is_ordered=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@require_POST
def cart_update(request, prod_pk):
    cart = CartItem.objects.filter(user=request.user, is_ordered=False)
    item = cart.get(product=Product.objects.get(pk=prod_pk))
    qty = int(request.POST.get('qty'))
    if qty <= 0:
        qty = 1
    elif qty > item.product.stock:
        qty = item.product.stock
    try:
        item.qty = qty
        item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        print('Error')


@require_POST
def cart_delete(request, prod_pk):
    cart = CartItem.objects.filter(user=request.user, is_ordered=False)
    try:
        cart.get(product=Product.objects.get(pk=prod_pk)).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        print('Error')


@login_required()
def cart_view(request):
    cart = CartItem.objects.filter(user=request.user, is_ordered=False)
    form = CartForm()

    def get_total(t_cart):
        sums = [it.product.price * it.qty for it in t_cart]
        return sum(sums)

    context = {
        'title': SITE_TITLE + 'Cart',
        'form': form,
        'total': get_total(cart),
        'cart': cart,
    }
    return render(request, 'cart_view.html', context | menu_context)


@login_required()
def order_view(request):
    new_order = Order1.objects.create(order_number=int(time.time()), user=request.user)
    cart = CartItem.objects.filter(user=request.user, is_ordered=False)

    if request.method == 'POST':
        for item in cart:
            item.order = new_order
            item.is_ordered = True
            item.save()
            item.product.stock -= item.qty
            item.product.save()
        return redirect(reverse('successful_order', kwargs={'order_number': new_order.order_number}))


@login_required()
def successful_order(request, order_number):
    return render(request, 'successful_order.html', {'order_number': order_number} | menu_context)


@login_required()
def my_orders(request):
    orders = Order1.objects.filter(user=request.user).order_by('-created')
    return render(request, 'my_orders.html', {'orders': orders} | menu_context)

