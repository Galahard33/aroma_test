from django.contrib import admin
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ShopAdminForm(forms.ModelForm):
    Content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Shop
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}


class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    form = ShopAdminForm
    list_display = ('id', 'title', 'price', 'views', 'category')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ("category",)
    readonly_fields = ('views',)
    fields = ('title', 'slug', 'price', 'category', 'subcategory', 'availability', 'photo', 'min_content', 'specifications', 'specifications2', 'Content', 'views')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_add', 'shop', 'date')
    list_filter = ('date', )
    search_fields = ('shop', 'user_add',)




class CartProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'qty', 'total_prise')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_product', 'total_prise')


class SubcategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_display = ('id', 'title', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order)
admin.site.register(Subcategories, SubcategoriesAdmin)

