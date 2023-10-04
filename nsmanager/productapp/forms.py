# myapp/forms.py
from django import forms
from .models import Product
from .models import Warehouse,User

class WarehouseForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Warehouse
        fields = ['name', 'url', 'credentials', 'users']
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
