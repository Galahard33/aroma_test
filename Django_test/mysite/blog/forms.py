from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':"Текст комментария", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Текст комментария'"}))

    class Meta:
        model = Comment
        fields = ('text',)