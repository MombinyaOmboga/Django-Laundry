from django import forms

from .models import Cart, Checkout, Service, ServiceCart


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

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['full_name', 'email_id', 'delivery_address','phone_number']