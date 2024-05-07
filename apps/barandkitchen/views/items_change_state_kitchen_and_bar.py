from django.shortcuts import redirect, render
from apps.cuentas.models import  Item
from django.contrib.auth.decorators import login_required 
from utils.product_validate.validate_ingredients_and_add_cant import validate_product_discount_ingredient


@login_required(login_url='/admin/login/')
def items_change_kitchen_view(request):
    error=''
    if request.POST:
        try:
            item_id = int(request.POST['item'])
            item = Item.objects.get(id=item_id)
            error = validate_product_discount_ingredient(item)
            if error =='':
                if item.state == "ordenado":
                    item.state = "preparando"
                    item.save()
                elif item.state == "preparando":
                    item.state = "finalizado"
                    item.save()
        except Item.DoesNotExist:
            error = "Ítem no encontrado."
        except ValueError:
            error = "ID de ítem inválido."
    context ={"error":error} 
    return render(request,'items_bar_and_kitchen.html',context)


@login_required(login_url='/admin/login/')
def items_change_bar_view(request):
    error=''
    if request.POST:
        try:
            item_id = int(request.POST['item'])
            item = Item.objects.get(id=item_id)
            error = validate_product_discount_ingredient(item)
            if error =='':
                if item.state == "ordenado":
                    item.state = "preparando"
                    item.save()
                elif item.state == "preparando":
                    item.state = "finalizado"
                    item.save()
        except Item.DoesNotExist:
            error = "Ítem no encontrado."
        except ValueError:
            error = "ID de ítem inválido."
    context ={"error":error} 
    return render(request,'items_bar_and_kitchen.html',context)


@login_required(login_url='/admin/login/')
def items_finish_bar_and_kitchen_view(request):
    error=''
    if request.POST:
        try:
            item_id = int(request.POST['item'])
            item = Item.objects.get(id=item_id)
            item.state = "finalizado"
            item.save()
        except Item.DoesNotExist:
            error = "Ítem no encontrado."
        except ValueError:
            error = "ID de ítem inválido."
    context ={"error":error} 
    return render(request,'items_bar_and_kitchen.html',context)
