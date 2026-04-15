from django import forms
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