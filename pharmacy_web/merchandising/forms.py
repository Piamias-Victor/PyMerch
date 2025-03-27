from django import forms
from .models import Pharmacy, PharmacyElement, Laboratory, Product

class PharmacyForm(forms.ModelForm):
    class Meta:
        model = Pharmacy
        fields = ['name', 'width', 'height']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PharmacyElementForm(forms.ModelForm):
    class Meta:
        model = PharmacyElement
        fields = ['name', 'element_type', 'x', 'y', 'width', 'height', 'orientation', 'laboratory']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'element_type': forms.Select(attrs={'class': 'form-select'}),
            'x': forms.NumberInput(attrs={'class': 'form-control'}),
            'y': forms.NumberInput(attrs={'class': 'form-control'}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'orientation': forms.Select(attrs={'class': 'form-select'}),
            'laboratory': forms.Select(attrs={'class': 'form-select'}),
        }

class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ['name', 'contact', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'laboratory', 'price', 'cost', 'stock', 'ean']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'laboratory': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'ean': forms.TextInput(attrs={'class': 'form-control'}),
        }