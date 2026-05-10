from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from allauth.account.forms import LoginForm
from captcha.fields import CaptchaField

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar', 'bio']
        widgets = {
            'nickname': forms.TextInput(attrs={
                'placeholder': '輸入你想顯示的暱稱'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': '寫一點自我介紹吧...'
            }),
        }


class CustomLoginForm(LoginForm):
    captcha = CaptchaField(
        label='圖形驗證碼',
        error_messages={
            'invalid': '驗證碼錯誤，請重新輸入。'
        }
    )


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label='Email'
    )

    captcha = CaptchaField(
        label='圖形驗證碼',
        error_messages={
            'invalid': '驗證碼錯誤，請重新輸入。'
        }
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'captcha'
        ]