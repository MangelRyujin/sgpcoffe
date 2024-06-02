from django.shortcuts import render,redirect
from apps.cuentas.forms.item_form import AddItemForm
from apps.cuentas.models import Item
from django.contrib.auth.decorators import login_required 


@login_required(login_url='/admin/login/')
def form_item_delete_view(request,pk,order):
    item = Item.objects.get(pk=pk)
    if request.method == "POST":
        if item.state == "ordenado":
            item.delete()
        else:
            item.state="cancelado"
            item.save()
        return redirect(f'/ventas/gestionar/cuenta/{order}')
    
    context = {"item": item,"order":order}

    return render(request, 'order_unpaid/delete_item_form.html',context)


@login_required(login_url='/admin/login/')
def form_create_add_item_view(request,pk,order):
    error=''
    item = Item.objects.get(pk=pk)
    form= AddItemForm(request.POST or None,product_id=item.product.id)
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
