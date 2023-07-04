from django.conf.urls.static import static
from django.urls import path
from .views import *
from store import settings

urlpatterns = [
    path('account/delete/', DeleteUser.as_view(), name='delete_user'),
    path('accounts/register/', RegisterUser.as_view(), name='register'),
    path('accounts/change_password/', ChangePassword.as_view(), name='change_password'),
    path('accounts/change_info/', ChangeUserInfo.as_view(), name='change_info'),
    path('accounts/logout/', PLogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/profile/my_orders', my_orders, name='my_orders'),
    path('accounts/profile/successful_order/<int:order_number>/', successful_order, name='successful_order'),
    path('accounts/profile/order/', order_view, name='order_view'),
    path('accounts/profile/cart_view/', cart_view, name='cart_view'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', PLoginView.as_view(), name='login'),
    path('cart_add/<int:prod_pk>/', cart_add, name='cart_add'),
    path('cart_update/<int:prod_pk>/', cart_update, name='cart_update'),
    path('cart_delete/<int:prod_pk>/', cart_delete, name='cart_delete'),
    path('search/', SearchView.as_view(), name='search'),
    path('cat/<str:cat_slug>/', CatView.as_view(), name='cat_view'),
    path('subcat/<str:subcat_slug>/', SubcatView.as_view(), name='subcat_view'),
    path('product/<str:product_slug>/', product_view, name='product_view'),
    path('', HomeView.as_view(), name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

