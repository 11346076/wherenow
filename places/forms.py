from django import forms
from .models import Place


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = [
            'category',
            'name',
            'area',
            'address',
            'google_map_link',
            'note',
            'budget',
            'image',
            'is_public',
            'shared_with_couple',
        ]
        labels = {
            'category': '分類',
            'name': '地點名稱',
            'area': '地區',
            'address': '地址',
            'google_map_link': 'Google 地圖連結',
            'note': '備註',
            'budget': '平均花費/人',
            'image': '地點照片',
            'is_public': '是否公開',
            'shared_with_couple': '是否與情侶共享',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '請輸入地點名稱'
            }),
            'area': forms.TextInput(attrs={
                'placeholder': '例如：台北市、中山區'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': '請輸入完整地址'
            }),
            'google_map_link': forms.URLInput(attrs={
                'placeholder': '請貼上 Google 地圖連結'
            }),
            'note': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': '寫一些備註...'
            }),
            'budget': forms.NumberInput(attrs={
                'placeholder': '例如：500'
            }),
        }