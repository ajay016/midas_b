from django import forms
from .models import MidasbuyAccount


class MidasbuyAccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    class Meta:
        model  = MidasbuyAccount
        fields = ["label", "email", "password", "phone"]
