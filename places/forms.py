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
        ]