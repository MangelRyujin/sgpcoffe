from django import forms
from apps.cuentas.models import Item, AddItem, ItemMotiveCancelMessage, UtilsItem,Order
from apps.mesas.models import Table
from apps.productos.models import Add, ProductAddRelation, UtilProduct
from django.core.exceptions import ValidationError



class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['table']    
        


class OrderTableForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['table']    
        
    def __init__(self, *args, product_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['table'].queryset = Table.objects.filter(active=True,state="libre").order_by('id')


class PaidOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['cash','transfer','paid_method']       
        
    def clean(self):
        cleaned_data = super().clean()
        cash = cleaned_data.get('cash')
        transfer = cleaned_data.get('transfer')

        if cash < 0 or transfer < 0:
            msg = "Los valores de 'cash' y 'transfer' deben ser mayores que 0."
            self.add_error(None, msg)
            raise ValidationError("error e")
        return cleaned_data

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
    
    def clean(self):
        cleaned_data = super().clean()
        cant = cleaned_data.get('cant')
        add = cleaned_data.get('add')

        if cant > add.stock.stock:

            raise ValidationError(f"No contiendes esa cantidad disponible. Máximo {add.stock.stock}.")
        return cleaned_data
        
    def __init__(self, *args, product_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if product_id:
            # Obtener todas las relaciones ProductAddRelation para el producto dado
            relations = ProductAddRelation.objects.filter(product=product_id)
            # Extraer los IDs de los objetos Add asociados
            add_ids = [relation.add_id for relation in relations]
            # Filtrar el queryset del campo 'add' basado en los IDs obtenidos
            self.fields['add'].queryset = Add.objects.filter(id__in=add_ids,stock__stock__gte=1)
            
class UtilItemForm(forms.ModelForm):
    
    class Meta:
        model = UtilsItem
        fields = ['cant', 'util']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['util'].queryset = UtilProduct.objects.filter(stock__stock__gte=1)
 
class ItemMotiveCancelMessageForm(forms.ModelForm):
    
    class Meta:
        model = ItemMotiveCancelMessage
        fields = ['motive']       


class OrderItemMessageForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ['message']    
        
        
class ItemChangeCantForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [ 'cant']