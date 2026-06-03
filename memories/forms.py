from django import forms
from django.forms import inlineformset_factory

from .models import Memory, MemoryPhoto
from places.models import Place


class MemoryForm(forms.ModelForm):
    place = forms.ModelChoiceField(
        queryset=Place.objects.none(),
        label='地點',
        widget=forms.Select(attrs={
            'class': 'select2',
            'required': True,
        })
    )

    visit_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='造訪日期'
    )

    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': '寫一些備註...'
        }),
        label='心得'
    )

    rating = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=5,
        initial=0,
        widget=forms.NumberInput(attrs={
            'placeholder': '0-5'
        }),
        label='評分'
    )

    cost = forms.IntegerField(
        required=False,
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            'placeholder': '例如：500'
        }),
        label='花費'
    )

    recommended = forms.BooleanField(
        required=False,
        label='是否推薦'
    )

    shared_with_couple = forms.BooleanField(
        required=False,
        label='是否與情侶共享'
    )

    is_public = forms.BooleanField(
        required=False,
        initial=True,
        label='是否公開'
    )

    class Meta:
        model = Memory
        fields = [
            'place',
            'visit_date',
            'rating',
            'cost',
            'comment',
            'recommended',
            'shared_with_couple',
            'is_public',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['place'].queryset = Place.objects.filter(user=user).order_by('-created_at')

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:
                field.widget.attrs['class'] = 'form-control'

        self.fields['comment'].widget.attrs['class'] = 'form-control'
        self.fields['recommended'].widget.attrs['class'] = 'form-check-input'
        self.fields['shared_with_couple'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_public'].widget.attrs['class'] = 'form-check-input'


MemoryPhotoInlineFormset = inlineformset_factory(
    Memory,
    MemoryPhoto,
    fields=('image',),
    extra=1,
    can_delete=True,
    widgets={
        'image': forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
        }),
    },
)
