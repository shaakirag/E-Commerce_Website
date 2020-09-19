from django.forms import ModelForm
from django import forms
from store.models import Product, Order, Image

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'featured',
            'price',
            'digital',
            'category',
            'tag'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control '}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'digital': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tag': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = [
            'product',
            'image'
        ]

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']
    