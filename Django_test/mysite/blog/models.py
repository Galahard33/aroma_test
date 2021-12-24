from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='url', unique=True)
    photo = models.ImageField(upload_to='photos/blog/categories/', verbose_name='Фото категории', blank=True)
    tagline = models.CharField(max_length=100, verbose_name='Слоган категории', blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={"slug_cat": self.slug})


class Tags(models.Model):
    title = models.CharField(max_length=200, verbose_name='Тег')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='url')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def get_absolute_url(self):
        return reverse('blog_tag', kwargs={"slug_tag": self.slug})


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    photo = models.ImageField(upload_to='photos/blog/', verbose_name='Картинка статьи')
    text = models.TextField(verbose_name='Текст статьи')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, verbose_name='Категории', related_name='blog_category')
    tags = models.ManyToManyField(Tags, blank=True, related_name='related_tag', verbose_name='Тэги')
    created_at = models.DateTimeField(auto_now=True,)
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    slug = models.SlugField(max_length=200, unique=True,)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={"slug_post": self.slug})


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    text = models.TextField()
    user_add = models.ForeignKey(User, related_name='user_blog', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='blog_item', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user_add, self.blog)

    class Meta:
        verbose_name = 'Коментарии'
        verbose_name_plural = 'Коментарии'


class Photo(models.Model):
    photo = models.ImageField(upload_to='photos/blog/photo/', verbose_name='Фото')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания')

    def __str__(self):
        return str(self.created_at)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
