from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug_cat": self.slug})


class Subcategories(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='related_subcategories')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('subcategories', kwargs={"slug_sub": self.slug,
                                                'slug_cat': self.category.slug})


class Shop(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название товара')
    photo = models.ImageField(upload_to='photos/', verbose_name='Картинка товара')
    price = models.IntegerField(verbose_name='Цена')
    availability = models.BooleanField(verbose_name='В наличи')
    min_content = models.TextField(blank=True, verbose_name='Краткое описание')
    specifications = models.TextField(verbose_name='Характеристки названия')
    specifications2 = models.TextField(verbose_name='Харакеристики значения')
    Content = models.TextField(verbose_name='Полное описание')
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='shop')
    subcategory = ChainedForeignKey(Subcategories,
                                    on_delete=models.PROTECT,
                                    related_name='subitem',
                                    null=True,
                                    chained_field="category",
                                    chained_model_field="category",
                                    show_all=False,
                                    auto_choose=True,
                                    sort=True)
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={"slug_cat": self.category.slug,
                                              "slug": self.slug,
                                              })

    class Meta:
        ordering = ['title']
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    text = models.TextField()
    user_add = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='shop_item', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user_add, self.shop)

    class Meta:
        verbose_name = 'Коментарии'
        verbose_name_plural = 'Коментарии'


class CartProduct(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, related_name='related_user')
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_cart')
    product = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='relates_product')
    qty = models.PositiveIntegerField(default=1)
    total_prise = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return '{}, {} шт, {} руб'.format(self.product, self.qty, self.total_prise)

    def save(self, *args, **kwargs):
        self.total_prise = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE, related_name='related_ovner', blank=True, null=True)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart_product')
    total_product = models.PositiveIntegerField(default=0)
    total_prise = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return 'Корзина:{}'.format(self.id)




class Order(models.Model):

        STATUS_NEW = 'new'
        STATUS_IN_PROGRESS = 'in_progress'
        STATUS_READY = 'is_ready'
        STATUS_COMPLETED = 'completed'

        STATUS_CHOICES = (
            (STATUS_NEW, 'Новый заказ'),
            (STATUS_IN_PROGRESS, 'В процессе'),
            (STATUS_READY, 'Готов'),
            (STATUS_COMPLETED, 'Выполнен')

        )
        customer = models.ForeignKey(User, verbose_name='Заказчик', on_delete=models.CASCADE, related_name='related_orders')
        first_name = models.CharField(max_length=150, verbose_name='Имя')
        last_name = models.CharField(max_length=150, verbose_name='Фамилия')
        phone = models.CharField(max_length=20, verbose_name='Телефон')
        address = models.CharField(max_length=250, verbose_name='Адрес')
        cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='related_cart_order', verbose_name='Корзина', null=True, blank=True)
        status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES,
                                  default=STATUS_NEW)
        comment = models.CharField(max_length=250, verbose_name='Комментарий к заказу', blank=True, null=True)
        created_at = models.DateTimeField(auto_now=True, verbose_name='Дата оздания заказа')

        def __str__(self):
            return str(self.id)
