from django.contrib import auth
from django.contrib.auth.models import User
from django.core import paginator
from django.db.models import Count
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from .models import Cart, CartProduct, Category


class CartMixins(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = auth.get_user(request)
            cart = Cart.objects.filter(in_order=False, owner=customer).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            customer = User.objects.filter(id=2).first()
            cart = Cart.objects.filter(id=3).first()
        self.customer = customer
        cart_product = CartProduct.objects.filter(user=self.customer)
        self.cart = cart
        self.cart_product = cart_product
        return super().dispatch(request, *args, **kwargs)


class CategoryMixins(View):
    def dispatch(self, request, slug_cat, *args, **kwargs):
        category = Category.objects.get(slug=slug_cat)
        subcategorys = category.related_subcategories.all().annotate(cnt=Count('subitem')).filter(cnt__gt=0)
        self.category = category
        self.subcategorys = subcategorys
        return super().dispatch(request, slug_cat, *args, **kwargs)


class PageMixins(View):
    def dispatch(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        self.page_number = page_number
        self.page_obj = page_obj