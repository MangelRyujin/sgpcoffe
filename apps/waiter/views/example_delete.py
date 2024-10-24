from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from apps.cuentas.models import AddItem, Item, Order, UtilsItem
from apps.productos.models import Category

@login_required(login_url='admin/login/')
def order_delete_view(request,pk):
    if request.POST:
        order = Order.objects.filter(pk=pk).first()
        table=order.table
        context={
            "table":table
        }
        if not order.order_delete:
            context['error']="No puedes eliminar la orden ya que existen pedidos en otros procesos"
            context['order']=order
            context['categories']=Category.objects.filter(type='vendible')
        else:
            
            table.state="libre"
            table.save()
            order.delete()
    response = render(request,'waiter/table.html',context)
    response['HX-Trigger']='update-table-list'
    return response    


@login_required(login_url='admin/login/')
def order_item_delete_view(request,pk):
    item = Item.objects.filter(pk=pk).first()
    context={}
    context['item']=item
    if request.POST:
        context['order']=item.order
        if item.state == "ordenado":
          item.delete()
        else:
            context["error"]="El pedido ya se encuentra en otro proceso"
        return render(request,'waiter/itemsResult.html',context)
    return render(request,'waiter/orderItemDelete/orderItemDeleteVerify.html',context)

@login_required(login_url='admin/login/')
def order_item_add_delete_view(request,pk):
    add_item = AddItem.objects.filter(pk=pk).first()
    context={}
    context['item']=add_item.item
    if add_item:
        add_item.delete()
    return render(request,'waiter/orderItemDetail/order_item_detail.html',context)

@login_required(login_url='admin/login/')
def order_item_utils_delete_view(request,pk):
    utils_item = UtilsItem.objects.filter(pk=pk).first()
    context={}
    context['item']=utils_item.item
    if utils_item:
        utils_item.delete()
    return render(request,'waiter/orderItemDetail/order_item_detail.html',context)
