from django import template
from django.db.models import Count

from blog.models import Category, Tags, Blog


register = template.Library()

@register.simple_tag()
def get_categories():
    category = Category.objects.all().annotate(cnt=Count('blog_category')).filter(cnt__gt=0)
    return category

@register.simple_tag()
def get_tags():
    return Tags.objects.all()


@register.simple_tag()
def get_pop_posts():
    return Blog.objects.all().order_by('-views')[:4]