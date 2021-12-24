from django.contrib import messages
from django.db.models import F
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from .mixins import *
from .forms import CommentForm


from .models import *


class Blogs(BlogMixin, View):
    def get(self, request, *args, **kwargs):
        post = Blog.objects.all()
        category = Category.objects.all()
        category_top_bar = Category.objects.filter(active=True)
        paginator = Paginator(post, 5)
        page_obj = paginator.get_page(self.page_number)
        photo = Photo.objects.order_by("-created_at")[:6]
        return render(request, 'blog/blog.html', context=({
            'post': post,
            'page_obj': page_obj,
            'category': category,
            'category_top_bar': category_top_bar,
            'photo':photo}))


def post_detail(request, slug_post, *args, **kwargs):
    post = Blog.objects.get(slug=slug_post)
    Blog.objects.filter(slug=slug_post).update(views=F('views') + 1)
    comments = post.blog_item.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            messages.success(request, 'Ваш коментарий отправлен на модерацию')
            new_comment = comment_form.save(commit=False)
            new_comment.blog = post
            new_comment.user_add = auth.get_user(request)
            new_comment.save()
            return HttpResponseRedirect('/')
    else:
        comment_form = CommentForm()
    return render(request, 'blog/single-blog.html', context=({
        'post': post,
        'comments': comments,
        'comment_form': comment_form}))


class GetCategory(BlogMixin, View):
    def get(self, request, slug_cat, *args, **kwargs):
        category_post = Category.objects.get(slug=slug_cat)
        post = category_post.blog_category.all()
        paginator = Paginator(post, 5)
        page_obj = paginator.get_page(self.page_number)
        return render(request, 'blog/blog.html', context=({
            'post': post,
            'page_obj': page_obj,
            'category_post': category_post}))


class GetTag(BlogMixin, View):
    def get(self, request, slug_tag, *args, **kwargs):
        tag_post = Tags.objects.get(slug=slug_tag)
        post = tag_post.related_tag.all()
        paginator = Paginator(post, 5)
        page_obj = paginator.get_page(self.page_number)
        return render(request, 'blog/blog.html', context=({
            'post': post,
            'page_obj': page_obj,
            'tag_post': tag_post}))