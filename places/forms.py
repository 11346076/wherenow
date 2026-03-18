from django import forms
from .models import Place


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = [
            'category',
            'name',
            'area',
            'google_map_link',
            'note',
            'budget',
            'is_public',
            'shared_with_couple',
        ]
        labels = {
            'category': '分類',
            'name': '地點名稱',
            'area': '地區',
            'google_map_link': 'Google 地圖連結',
            'note': '備註',
            'budget': '預算',
            'is_public': '是否公開',
            'shared_with_couple': '是否與情侶共享',
        }