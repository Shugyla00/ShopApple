from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from shop.models import Order


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class AddCartForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'item']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'phoneNumber', 'first_name', 'last_name']
        widgets = {
            # 'avatar': forms.FileInput(),
            'bio': forms.Textarea(),
        }
