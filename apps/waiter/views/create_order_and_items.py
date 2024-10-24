from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse

from apps.cuentas.forms.item_form import AddItemForm, ItemForm, UtilItemForm
from apps.cuentas.models import Item, Order, Shift
from apps.mesas.models import Table
from apps.productos.models import Category, Product

@login_required(login_url='admin/login/')
def order_create_view(request,pk):
    if request.POST:
        table = Table.objects.filter(pk=pk).first()
        order=Order.objects.create(
            is_paid="no pagada",
            paid_method="efectivo",
            transfer = 0,
            cash = 0,
            shift = Shift.objects.filter(active=True).first(),
            table = table,
            user = request.user,
        )
        if table.delivered == False:
            table.state = "ocupada"
            table.save()
        
        context={
            'order':order,
            'table':table,
            'categories': Category.objects.filter(type='vendible')
        }
        response= render(request,'waiter/table.html',context)
        response['HX-Trigger']='update-table-list'
        return response

@login_required(login_url='admin/login/')
def product_list_results(request,pk):
    order = Order.objects.filter(pk=pk).first()
    get_copy = request.GET.copy()
    category=get_copy.get('categories') or None
    products = Product.objects.filter(active=True,categories=category)
    context={
        'order':order,
        'category':category,
        'products': products
    }
    return render(request,'waiter/products/products_list_result.html',context)

@login_required(login_url='admin/login/')
def order_item_create_view(request,pk):
    if request.POST:
        order = Order.objects.filter(pk=pk).first()
        products= Product.objects.filter(categories=request.GET.get('category'))
        product = Product.objects.filter(pk=request.GET.get('product')).first()
        context={
            'order':order,
            'products':products,
            'category':request.GET.get('category'),
        }
        if product:
            if product.cant_discount_ingredients(request.POST['cant']):
                Item.objects.create(
                order=order,
                product=product,
                cant=request.POST['cant'],
                type = 'llevar' if request.POST.get('type') else 'local'
                )
                context['message']=f"{product.name} añadido correctamente"
            else:
                context['error'] = f"{product.name} no puede ser pedido ya que no existe cantidad existente"
        return render(request,'waiter/products/products_list_result.html',context)
    
    
@login_required(login_url='admin/login/')
def order_item_add_create(request,pk):
    item = Item.objects.filter(pk=pk).first()
    form=AddItemForm(product_id=item.product.pk)
    context={
            'item':item,
            'order':item.pk,
            
        }
    if request.POST:
        form=AddItemForm(request.POST)
        if form.is_valid():
            item_add = form.save(commit=False)
            item_add.item=item
            item_add.save()
            context['message']=f"Agregado añadido correctamente"
        else:
            context['error']=form.errors
    context['form']=form    
    return render(request,'waiter/orderItemAdd/orderItemAddForm.html',context)

@login_required(login_url='admin/login/')
def order_item_util_create(request,pk):
    item = Item.objects.filter(pk=pk).first()
    form=UtilItemForm()
    context={
            'item':item,
            'order':item.pk,
            
        }
    if request.POST:
        form=UtilItemForm(request.POST)
        if form.is_valid():
            item_util = form.save(commit=False)
            item_util.item=item
            item_util.save()
            context['message']=f"Útil añadido correctamente"
        else:
            context['error']=form.errors
    context['form']=form    
    return render(request,'waiter/orderItemUtil/orderItemUtilForm.html',context)