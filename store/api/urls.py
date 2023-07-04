from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [
    path('drf-auth/', include('rest_framework.urls')),
    path('cat/<str:cat_slug>/', CatAPIList.as_view()),
    path('subcat/<str:subcat_slug>/', SubcatAPIList.as_view()),
    path('products/', ProductAPIList.as_view()),
    path('product/<str:product_slug>/', ProductAPIDetail.as_view()),
    path('review/<str:product_slug>/', ListAPIReview.as_view()),
    path('orders/', OrderAPIView.as_view()),
]

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart_item')
router.register(r'users', UserViewSet, basename='user')

urlpatterns += [
    path('', include(router.urls)),
]
