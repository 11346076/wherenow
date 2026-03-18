from django import forms

class CoupleInvitationForm(forms.Form):
    receiver_username = forms.CharField(
        max_length=150,
        label='對方帳號'
    )