from django import forms
from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}


class BlogAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = '__all__'


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    form = BlogAdminForm
    list_display = ('id', 'title', 'views')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ("category",)
    readonly_fields = ('views',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Comment)
admin.site.register(Photo)
