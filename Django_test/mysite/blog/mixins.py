from django.contrib import auth
from django.contrib.auth.models import User
from django.core import paginator
from django.core.paginator import Paginator
from django.db.models import Count
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View


from .models import Blog, Category, Tags

class BlogMixin(View):
    def dispatch(self, request, *args, **kwargs):
        page_number = request.GET.get('page', 1)
        self.page_number = page_number
        return super().dispatch(request, *args, **kwargs)