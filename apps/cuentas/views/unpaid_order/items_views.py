from django.shortcuts import render,redirect
from apps.cuentas.forms.item_form import AddItemForm, ItemMotiveCancelMessageForm, UtilItemForm
from apps.cuentas.models import Item, ItemMotiveCancelMessage
from django.contrib.auth.decorators import login_required 


@login_required(login_url='/admin/login/')
def form_item_delete_view(request,pk,order):
    item = Item.objects.get(pk=pk)
    form = ItemMotiveCancelMessageForm()
    if request.method == "POST":
        if item.state == "ordenado":
            item.delete()
        else:
            ItemMotiveCancelMessage.objects.create(
                item=item,
                motive=request.POST.get("motive")
            )
            item.state="cancelado"
            item.save()
            return redirect(f'/ventas/gestionar/cuenta/{order}')
    
    context = {"item": item,"order":order,"form":form}

    return render(request, 'order_unpaid/delete_item_form.html',context)


@login_required(login_url='/admin/login/')
def form_create_add_item_view(request,pk,order):
    error=''
    item = Item.objects.get(pk=pk)
    form=[]
    is_add_form= AddItemForm(request.POST or None,product_id=item.product.id)
    if is_add_form["add"].__len__() > 1:
       form = is_add_form
    elif is_add_form["add"].__len__() == 1:
        error="No contiene ningun agregado relacionado"
    if item.state != "ordenado":
        error="No puede añadir agregados ya que el pedido esta en otro estado"
    if request.method == "POST":
        if form.is_valid():
            item_add = form.save(commit=False)
            item_add.item=item
            item_add.save()
        return redirect(f'/ventas/gestionar/cuenta/{order}')
    
    context = {"item": item,"order":order,"form":form,"error":error}

    return render(request, 'order_unpaid/create_add_item_form.html',context)


@login_required(login_url='/admin/login/')
def form_create_util_item_view(request,pk,order):
    error=''
    item = Item.objects.get(pk=pk)
    form=[]
    is_util_form= UtilItemForm(request.POST or None)
    if is_util_form["util"].__len__() > 1:
       form = is_util_form
    elif is_util_form["util"].__len__() == 1:
        error="No existen útiles"
    if item.state != "ordenado":
        error="No puede añadir útiles ya que el pedido esta en otro estado"
    if request.method == "POST":
        if form.is_valid():
            item_util = form.save(commit=False)
            item_util.item=item
            item_util.save()
        return redirect(f'/ventas/gestionar/cuenta/{order}')
    
    context = {"item": item,"order":order,"form":form,"error":error}

    return render(request, 'order_unpaid/create_util_item_form.html',context)