from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Comment, Order


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Username", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Username'"}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':"Password", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Password'"}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control',  'placeholder':"Confirm Password", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Confirm Password'"}))
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':"Email Address", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Email Address'"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Username", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Username'"}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':"Password", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Password'"}))


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':"Текст комментария", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Текст комментария'"}))

    class Meta:
        model = Comment
        fields = ('text',)


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Имя", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Имя'"}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Фамилия", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Фамилия'"}))
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Телефон", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Телефон'"}))
    address = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Адрес", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Адрес'"}))
    comment = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Комментарий", 'onfocus':"this.placeholder = ''" , 'onblur':"this.placeholder = 'Комментарий'"}))

    class Meta:
        model = Order
        fields = ('first_name','last_name', 'phone', 'address')