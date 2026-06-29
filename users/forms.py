from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from allauth.account.forms import LoginForm
from allauth.account.models import EmailAddress
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'autocomplete': 'username',
            'placeholder': '輸入帳號或 Email',
        })
        self.fields['password'].widget.attrs.update({
            'autocomplete': 'current-password',
            'placeholder': '輸入密碼',
        })
        self.fields['captcha'].widget.attrs.update({
            'autocomplete': 'off',
            'placeholder': '輸入圖片中的文字',
        })


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username',
            'placeholder': '輸入帳號',
        })
        self.fields['email'].widget.attrs.update({
            'autocomplete': 'email',
            'placeholder': '輸入 Email',
        })
        self.fields['password1'].widget.attrs.update({
            'autocomplete': 'new-password',
            'placeholder': '輸入密碼',
        })
        self.fields['password2'].widget.attrs.update({
            'autocomplete': 'new-password',
            'placeholder': '再次輸入密碼',
        })
        self.fields['captcha'].widget.attrs.update({
            'autocomplete': 'off',
            'placeholder': '輸入圖片中的文字',
        })

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                '這個 Email 已經註冊過，請直接登入或使用 Google 登入綁定同一個帳號。'
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={
                    'primary': True,
                    'verified': False,
                },
            )

        return user
