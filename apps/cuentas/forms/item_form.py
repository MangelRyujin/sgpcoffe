from django import forms
from apps.cuentas.models import Item, AddItem
from apps.productos.models import Add

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [ 'type', 'cant']
        labels = {
			'type': 'Tipo',
			'cant':'Cantidad',
		}
        
class AddItemForm(forms.ModelForm):
    class Meta:
        model = AddItem
        fields = ['cant', 'add']