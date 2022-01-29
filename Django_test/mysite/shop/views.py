from django import http
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .models import *
from  blog.models import Blog, Comment
from django.core.paginator import Paginator
from django.db.models import F
from django.contrib import messages, auth
from .forms import UserRegisterForm, UserLoginForm, CommentForm, OrderForm
from django.contrib.auth import login, logout
from .mixins import CartMixins, CategoryMixins
from .utils import recalc_cart


class Index(CartMixins, View):
    def get(self, request, *args, **kwargs):
        shop = Shop.objects.all().order_by('-views')[:8]
        blog = Blog.objects.all().order_by('-views')[:3]
        return render(request, 'shop/index.html', context=({'shop': shop,
                                                            'cart': self.cart,
                                                            'blog': blog,

                                                            }))


class ShopCategory(View):
    def get(self, request, *args, **kwargs):
        shops = Shop.objects.all()
        paginator = Paginator(shops, 9)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        search_query = request.GET.get('search', '')
        if search_query:
            page_obj = Shop.objects.filter(title__icontains=search_query)
        else:
            Shop.objects.all()
        context = {
            'shops': shops,
            'page_obj': page_obj,
        }
        return render(request, 'shop/category.html', context=context)


class GetCategory(CategoryMixins, View):
    def get(self, request, slug_cat, *args, **kwargs):
        shops = self.category.shop.all()
        paginator = Paginator(shops, 6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'shop/categorys.html', context={'category': self.category,
                                                               'page_obj': page_obj,
                                                               'shops': shops,
                                                               'subcategorys': self.subcategorys})


class GetSubcategory(CategoryMixins, View):
    def get(self, request, slug_cat, slug_sub, *args, **kwargs):
        subcategory = Subcategories.objects.get(slug=slug_sub)
        shops = subcategory.subitem.all()
        paginator = Paginator(shops, 6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'shop/subcategories.html', context={
            'page_obj': page_obj,
            'subcategorys': self.subcategorys,
            'category': self.category
        })

def get_item_detail(request, slug_cat, slug, *args, **kwargs):
    item = Shop.objects.get(slug=slug)
    Shop.objects.filter(slug=slug).update(views=F('views') + 1)
    comments = item.shop_item.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            messages.success(request, 'Ваш коментарий отправлен на модерацию')
            new_comment = comment_form.save(commit=False)
            new_comment.shop = item
            new_comment.user_add = auth.get_user(request)
            new_comment.save()
            return http.HttpResponseRedirect('/')
    else:
        comment_form = CommentForm()
    return render(request, 'shop/item_detail.html', context={'item': item,
                                                                 'comment_form': comment_form,
                                                                 'comments': comments})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно заригистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка')
    else:
        form = UserRegisterForm()
    return render(request, 'shop/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'shop/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('home')


def contact(request):
    return render(request, 'shop/contact.html')


class AddToCartView(CartMixins, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            prod_sug = kwargs.get('slug')
            product = Shop.objects.get(slug= prod_sug)
            cart_product, created = CartProduct.objects.get_or_create(
                user=self.cart.owner, cart=self.cart, product=product, total_prise=product.price
            )
            if created:
                self.cart.products.add(cart_product)
            return HttpResponseRedirect('/cart/')
        else:
            messages.error(request, 'Авторизируйтесь что-бы добавить товар в корзину')


class DeleteToCartView(CartMixins, View):

    def get(self, request, *args, **kwargs):
        prod_sug = kwargs.get('slug')
        product = Shop.objects.get(slug=prod_sug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
            )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        return HttpResponseRedirect('/cart/')


class ChangeCount(CartMixins, View):
    def post(self, request, *args, **kwargs):
        prod_sug = kwargs.get('slug')
        product = Shop.objects.get(slug=prod_sug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        return HttpResponseRedirect('/cart')


class CartView(CartMixins, View):
    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
            'cart_product': self.cart_product
        }
        recalc_cart(self.cart)
        return render(request, 'shop/cart.html', context)


class Checkout(CartMixins, View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        context = {
            'cart': self.cart,
            'cart_product': self.cart_product,
            'form': form
        }

        return render(request, 'shop/checkout.html', context)


class MakeOrder(CartMixins, View):

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = auth.get_user(request)
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            new_order.cart = self.cart
            self.cart.save()
            new_order.save()
            messages.add_message(request, messages.INFO, 'Спасибо за заказ')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout')


