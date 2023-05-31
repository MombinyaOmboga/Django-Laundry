from django import forms
from .models import Service

class AddserviceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name',
                  'price']