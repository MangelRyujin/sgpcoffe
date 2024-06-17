from django.shortcuts import redirect, render
from apps.cuentas.models import  AddItem, Item,UtilsItem
from django.contrib.auth.decorators import login_required 
from apps.productos.models import Add, ProductAddRelation
from utils.product_validate.validate_ingredients_and_add_cant import validate_product_discount_ingredient


@login_required(login_url='/admin/login/')
def items_change_kitchen_view(request):
    error=''
    if request.POST:
        try:
            item_id = int(request.POST['item'])
            item = Item.objects.get(id=item_id)
            item.total_price=item.estimate_price
            error = validate_product_discount_ingredient(item)
            if error =='':
                if item.state == "ordenado":
                    item.state = "preparando"
                    item.revenue_price=item.revenue
                    item.product.discount_ingredients(item.cant)
                    for add in AddItem.objects.filter(item=item):
                        product_add = ProductAddRelation.objects.get(add=add.add.id,product=item.product.id)
                        product_add.discount_add(item.cant,add.cant)
                    for util in UtilsItem.objects.filter(item=item):
                        util.discount_util()
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
            item.total_price=item.estimate_price
            error = validate_product_discount_ingredient(item)
            if error =='':
                if item.state == "ordenado":
                    item.state = "preparando"
                    item.revenue_price=item.revenue
                    item.product.discount_ingredients(item.cant)
                    for add in AddItem.objects.filter(item=item):
                        product_add = ProductAddRelation.objects.get(add=add.add.id,product=item.product.id)
                        product_add.discount_add(item.cant,add.cant)
                    for util in UtilsItem.objects.filter(item=item):
                        util.discount_util()
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
