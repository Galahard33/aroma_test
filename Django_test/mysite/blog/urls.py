from django.urls import path
from .views import *


urlpatterns = [
    path('', Blogs.as_view(), name='blog'),
    path('post/<str:slug_post>/', post_detail, name='blog_detail'),
    path('post/category/<str:slug_cat>/', GetCategory.as_view(), name='blog_category'),
    path('post/tag/<str:slug_tag>/', GetTag.as_view(), name='blog_tag'),



]
