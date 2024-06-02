from django.shortcuts import render,redirect
from apps.cuentas.forms.item_form import  AddItemForm, ItemForm
from apps.cuentas.models import AddItem, Item, Order
from django.contrib.auth.decorators import login_required 
from django.forms import modelformset_factory

from apps.productos.models import Category, Product


@login_required(login_url='/admin/login/')
def unpaid_order_detail_view(request, pk):
    order = Order.objects.get(pk=pk)
    categories= Category.objects.filter(type="vendible")
    items_delivered = []
    for item in Item.objects.filter(order=order):
        items_delivered.append({
            'delivered': item,
            'add': AddItem.objects.filter(item=item)
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
