from django import template
from django.db.models import Count

from shop.models import Category, Subcategories

register = template.Library()


@register.inclusion_tag('inc/list_categories.html')
def get_categories_count():
    categories = Category.objects.annotate(cnt=Count('shop')).filter(cnt__gt=0)
    return {'categories': categories
            }






