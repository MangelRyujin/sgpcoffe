from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from apps.cuentas.forms.item_form import ItemMotiveCancelMessageForm
from apps.cuentas.models import Item

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