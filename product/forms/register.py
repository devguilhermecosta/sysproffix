from django import forms
from product.models import Product, ProductGroup
from utils.strings.normalize import normalize


class ProductRegisterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'group',
            'code',
            'name'
        ]

    def clean_name(self):
        name = self.cleaned_data["name"]
        return normalize(name)


class ProductGroupRegisterForm(forms.ModelForm):
    class Meta:
        model = ProductGroup
        fields = [
            'name',
        ]

    def clean_name(self):
        name = self.cleaned_data["name"]
        return normalize(name)
