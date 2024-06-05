from django.shortcuts import render,redirect
from apps.cuentas.forms.item_form import  AddItemForm, ItemForm, OrderForm, OrderTableForm, PaidOrderForm
from apps.cuentas.models import AddItem, Item, ItemMotiveCancelMessage, Order,UtilsItem
from django.contrib.auth.decorators import login_required 
from django.forms import modelformset_factory

from apps.mesas.models import Table
from apps.productos.models import Category, Product


@login_required(login_url='/admin/login/')
def unpaid_order_detail_view(request, pk):
    order = Order.objects.get(pk=pk)
    categories= Category.objects.filter(type="vendible")
    items_delivered = []
    for item in Item.objects.filter(order=order).order_by("-id"):
        items_delivered.append({
            'delivered': item,
            'add': AddItem.objects.filter(item=item),
            'util': UtilsItem.objects.filter(item=item),
            'motive':ItemMotiveCancelMessage.objects.filter(item=item).first()
        })

    context = {"order": order,"categories":categories, "items_delivered": items_delivered}

    return render(request, 'order_unpaid/unpaid_order_detail.html', context)


@login_required(login_url='/admin/login/')
def form_item_create_view(request,pk,order):
    product = Product.objects.get(pk=pk)
    form = ItemForm() 
    order_instance = Order.objects.get(pk=order)
    if request.method == "POST":
        print("hola")
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.product = product
            item.order = order_instance
            item.save()
        return redirect(f'/ventas/gestionar/cuenta/{order}')
    
    context = {"product": product, "form": form,"order":order}

    return render(request, 'order_unpaid/create_item_form.html',context)

@login_required(login_url='/admin/login/')
def product_sell_view(request,order):
    categories= Category.objects.filter(type="vendible")
    category= Category.objects.filter(type="vendible").first()
    products = Product.objects.filter(active=True,categories=category) 
    list_shell = []  # Aqui se puede hacer un filtro para mostrar los productos que al menos puedan pedirse 1 o mas veces
    if request.method == "POST":
        products = Product.objects.filter(active=True,categories=request.POST.get('category'))
    
    context = {"categories":categories,"products": products,"order":order}

    return render(request, 'order_unpaid/products_shell.html',context)



@login_required(login_url='/admin/login/')
def form_order_paid_view(request,pk):
    order = Order.objects.get(pk=pk)
    error=''
    form = PaidOrderForm(request.POST or None)
    if request.method == "POST":
        if float(request.POST.get("cash")) >= 0 and float(request.POST.get("transfer")) >= 0:
            order.paid_method= request.POST.get("paid_method")
            order.is_paid="pagada"
            order.cash = request.POST.get("cash")
            order.transfer = request.POST.get("transfer")
            order.table.state="libre"
            order.save()
            order.table.save()
            return redirect(f'/ventas/gestionar/cuentas/')
        else:
            error="Verifique que los montos sean válidos y que tenga todas los pedidos estén ya entregados o cancelados"
            return redirect(f'/ventas/gestionar/cuenta/{order.id}?error={error}')
    context = {"order":order,"error":error,"form":form}

    return render(request, 'order_unpaid/paid_order_form.html',context)

@login_required(login_url='/admin/login/')
def form_change_order_view(request,pk):
    order = Order.objects.get(pk=pk)
    error=''
    form = OrderTableForm(request.POST or None)
    if request.method == "POST":
        table= Table.objects.get(id=request.POST.get("table"))
        if table.state == "libre":
            order.table.state="libre"
            order.table.save()
            order.table=table
            if table.delivered == False:
                table.state="ocupada"
                table.save()
            order.save()
            return redirect(f'/ventas/gestionar/cuenta/{pk}')
        else:
            error="Esa mesa ya esta ocupada o no disponible"
            return redirect(f'/ventas/gestionar/cuenta/{order.id}?error={error}')
    context = {"order":order,"error":error,"form":form}

    return render(request, 'order_unpaid/change_table_order_form.html',context)