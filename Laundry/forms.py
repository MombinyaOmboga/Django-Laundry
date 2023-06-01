from django import forms
from .models import Service, Cart

class AddServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price']

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['clothes_amount']
