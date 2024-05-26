from django.shortcuts import render,redirect
from apps.cuentas.forms.item_form import  AddItemForm, ItemForm
from apps.cuentas.models import AddItem, Item, Order
from django.contrib.auth.decorators import login_required 
from django.forms import modelformset_factory

from apps.productos.models import Category, Product


@login_required(login_url='/admin/login/')
def unpaid_order_detail_view(request, pk):
    order = Order.objects.filter(pk=pk).first()
    products= Product.objects.filter(active=True)
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
    AddItemFormset = modelformset_factory(AddItem, form=AddItemForm)
    # Validar los formularios 
    order_instance = Order.objects.get(pk=order)
    
    if request.method == "POST":
        print("hola")
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)  # Guarda el objeto pero no lo guarda en la base de datos aún
            item.product = product  # Asigna el producto al que pertenece el ítem
            item.order = order_instance
            # item.save()
    #         item.save()  # Guarda el objeto en la base de datos
            # Procesamiento del formset
            formset = AddItemFormset(request.POST, queryset=AddItem.objects.none(), prefix='addItem')
            if formset.is_valid():
                for form_data in formset:
                    if form_data.is_valid():
                        form_data.instance.item=item
                        print(form_data.instance)
            else:
                print(formset.errors)
    #                     form_data.instance.product = product  # Asigna el producto al que pertenece el ítem
    #                     form_data.save()  # Guarda el objeto en la base de datos
        return redirect(f'/ventas/gestionar/cuenta/{order}')
    form = ItemForm()
    formset = AddItemFormset(request.POST or None, queryset= AddItem.objects.none(), prefix='addItem')	
    context = {"product": product, "form": form, "formset": formset ,"order":order}

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
