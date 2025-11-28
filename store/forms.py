from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "author", "sku", "purchase_price", "sale_price", "quantity"]
        labels = {
            "title": "Sarlavha",
            "author": "Muallif",
            "sku": "SKU / ISBN",
            "purchase_price": "Sotib olish narxi",
            "sale_price": "Sotish narxi",
            "quantity": "Miqdor",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Kitob nomi"}),
            "author": forms.TextInput(attrs={"class": "form-control", "placeholder": "Muallif (ixtiyoriy)"}),
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "SKU / ISBN"}),
            "purchase_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "sale_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }
