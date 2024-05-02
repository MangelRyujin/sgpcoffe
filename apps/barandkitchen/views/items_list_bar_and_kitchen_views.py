from django.shortcuts import render
from apps.cuentas.order_filter import OrderFilter 
from apps.cuentas.models import AddItem, Item, Order
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from apps.mesas.models import Table


@login_required(login_url='/admin/login/')
def items_list_bar_and_kitchen_view(request):
    error=''
    if request.POST:
        try:
            item_id = int(request.POST['item'])
            item = Item.objects.get(id=item_id)
            if item.state == "ordenado":
                item.state = "finalizado"
                item.save()
            error = ""
        except Item.DoesNotExist:
            error = "Ítem no encontrado."
        except ValueError:
            error = "ID de ítem inválido."
        
    bar=[]
    kitchen=[]
    for item in Item.objects.filter(state="ordenado",product__place="bar"):
       bar.append({
           'bar':item,
           'add': AddItem.objects.filter(
                            item = item
                        )
       })
    for item in Item.objects.filter(state="ordenado",product__place="cocina"):
       kitchen.append({
           'kitchen':item,
           'add': AddItem.objects.filter(
                            item = item
                        )
       })
    context ={"bars":bar,"kitchens":kitchen,"error":error} 
    return render(request,'items_bar_and_kitchen.html',context)