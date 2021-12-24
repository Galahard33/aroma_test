from django.urls import path

from .views import *


urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('shop_category/', ShopCategory.as_view(), name='shop_category'),
    path('register/', register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('shop_category/<str:slug_cat>/<str:slug_sub>/', GetSubcategory.as_view(), name='subcategories'),
    path('shop_category/<str:slug_cat>/', GetCategory.as_view(), name='category'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', DeleteToCartView.as_view(), name='remove_from_cart'),
    path('change-count/<str:slug>/', ChangeCount.as_view(), name='change_count'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('make-order/', MakeOrder.as_view(), name='make_order'),
    path('<str:slug_cat>/<str:slug>/', get_item_detail, name='item_detail'),

]