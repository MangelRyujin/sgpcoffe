from django import forms
from apps.cuentas.models import Item, AddItem, ItemMotiveCancelMessage, UtilsItem
from apps.productos.models import Add, ProductAddRelation, UtilProduct

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
