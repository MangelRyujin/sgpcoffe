from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from apps.cuentas.forms.item_form import ItemChangeCantForm, ItemForm, ItemMotiveCancelMessageForm
from apps.cuentas.models import AddItem, Item, Order, UtilsItem
from apps.productos.models import Category, ProductAddRelation
from apps.waiter.utils.ingredients_items import create_ingredients_item, remove_ingredients_item
from apps.waiter.utils.items_chage_cant import decrement_change_cant, increase_change_cant
from utils.product_validate.validate_ingredients_and_add_cant import validate_product_discount_ingredient

@login_required(login_url='admin/login/')
def order_item_check_view(request,pk):
    item = Item.objects.filter(pk=pk).first()
    if not item.is_active:
        item.is_active =True
        item.save()
    context={
        'item':item
    }
    return render(request,'waiter/orderItemDetail/order_item_detail.html',context)

@login_required(login_url='admin/login/')
def order_item_revert_view(request,pk):
    item = Item.objects.filter(pk=pk).first()
    if item.is_active:
        item.is_active =False
        item.save()
    context={
        'item':item
    }
    return render(request,'waiter/orderItemDetail/order_item_detail.html',context)


@login_required(login_url='admin/login/')
def order_item_cancel_view(request,pk):
    item = Item.objects.filter(pk=pk).first()
    form = ItemMotiveCancelMessageForm()
    context={}
    if item:
        if request.POST:
            form=ItemMotiveCancelMessageForm(request.POST)
            if form.is_valid():
                form_message = form.save(commit=False)
                form_message.item=item
                form_message.save()
                item.state = "cancelado"
                item.total_price = 0
                item.revenue_price = f'{item.cost_price}'
                item.save()
                context['item']=item
                return render(request,'waiter/orderItemDetail/order_item_detail.html',context)
    context['item']=item
    context['form']=form
    return render(request,'waiter/orderItemCancel/orderItemCancelVerify.html',context)


@login_required(login_url='admin/login/')
def order_item_delivery_view(request,pk):
    item = Item.objects.filter(pk=pk).first()
    if item.state == "finalizado":
        item.state = "entregado"
        item.total_price = item.estimate_price
        item.save()
    context={
        'item':item
    }
    return render(request,'waiter/orderItemDetail/order_item_detail.html',context)

@login_required(login_url='admin/login/')
def order_item_delivery_waiter_view(request,pk):
    item = Item.objects.filter(pk=pk).first()
    error=''
    if item.state == "ordenado" and item.product.place == "dependiente":
        try:
            error = validate_product_discount_ingredient(item)
            if error =='':
                item.revenue_price=item.revenue
                item.cost_price = item.inversion_cost
                create_ingredients_item(item)
                item.product.discount_ingredients(item.cant)
                for add in AddItem.objects.filter(item=item):
                    product_add = ProductAddRelation.objects.get(add=add.add.id,product=item.product.id)
                    product_add.discount_add(item.cant,add.cant)
                for util in UtilsItem.objects.filter(item=item):
                    util.discount_util()
                item.state = "entregado"
                item.total_price = item.estimate_price
                item.save()
        except Item.DoesNotExist:
            error = "Ítem no encontrado."
        except ValueError:
            error = "ID de ítem inválido."
        
    context={
        'item':item,
        'error':error
    }
    return render(request,'waiter/orderItemDetail/order_item_detail.html',context)


@login_required(login_url='/admin/login/')
def items_change_waiter_delivery_view(request):
    error=''
    if request.POST:
        try:
            item_id = int(request.POST['item'])
            item = Item.objects.get(id=item_id)
            item.total_price=item.estimate_price
            error = validate_product_discount_ingredient(item)
            if error =='':
                if item.state == "ordenado":
                    item.state = "entregado"
                    item.revenue_price=item.revenue
                    item.cost_price = item.inversion_cost
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


@login_required(login_url='admin/login/')
def order_item_check_all_view(request,pk):
    order= Order.objects.filter(table=pk,is_paid='no pagada').first()
    items = Item.objects.filter(order=order,is_active=False,state="ordenado")
    for item in items:
        item.is_active =True
        item.save()
    context={
        "order":order,
        "table":order.table,
        'categories': Category.objects.filter(type='vendible')
    }
    return render(request,'waiter/table.html',context)

@login_required(login_url='admin/login/')
def order_item_revert_all_view(request,pk):
    order= Order.objects.filter(table=pk,is_paid='no pagada').first()
    items = Item.objects.filter(order=order,is_active=True,state="ordenado")
    for item in items:
        item.is_active =False
        item.save()
    context={
        "order":order,
        "table":order.table,
        'categories': Category.objects.filter(type='vendible')
    }
    return render(request,'waiter/table.html',context)

@login_required(login_url='admin/login/')
def order_item_change_cant_view(request,pk):
    item = Item.objects.filter(pk=pk).first()
    context={
        "item":item,
    }
    message=''
    error=''
    form=ItemChangeCantForm(instance=item)
    if request.POST:
        cant=item.cant
        form=ItemChangeCantForm(request.POST,instance=item)
        if form.is_valid():
            cant_edit= cant - int(request.POST['cant'])
            if item.state != "ordenado":
                if cant < int(request.POST['cant']):
                    message,error =increase_change_cant(item,cant_edit*-1)
                elif cant > int(request.POST['cant']):
                    message =decrement_change_cant(item,cant_edit)
                else:
                    message=f"Se mantiene la misma cantidad"
            if error:
                context['error']=error
            if message:
                context['message']=message
            if message == '':
                context['message']="Cantidad editada correctamente"
            item=form.save(commit=False)
            item.total_price= item.estimate_price
            item.save()
            remove_ingredients_item(item)
    context['form']=form
    return render(request,'waiter/orderItemCantChange/orderItemCantChangeForm.html',context)