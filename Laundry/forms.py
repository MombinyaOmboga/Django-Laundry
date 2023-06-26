from django import forms
from .models import Service, Cart, ServiceCart

class AddServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price']

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['clothes_amount']

class AddServiceToCartForm(forms.ModelForm):
    class Meta:
        model = ServiceCart
        fields = ['service']