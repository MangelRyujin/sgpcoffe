from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse

from apps.cuentas.forms.item_form import OrderTableForm
from apps.cuentas.models import Item, Order, Shift
from apps.mesas.models import Table
from apps.productos.models import Category
from apps.waiter.order_forms import CreateOrderSoldForm
from apps.waiter.utils.order import order_paid_proccess_data

@login_required(login_url='admin/login/')
def order_detail_delivery_table_view(request,pk):
    shift=Shift.objects.filter(active=True).first()
    if shift is None:
        return redirect('/')
    order = Order.objects.filter(pk=pk,is_paid='no pagada').first()
    context={
        'order':order,
        'table':order.table,
        'categories':Category.objects.filter(type='vendible')
        }
    
    return render(request,'waiter/deliveryTable/order_detail.html',context)


@login_required(login_url='admin/login/')
def reload_order_detail_delivery_table_view(request,pk):
    order = Order.objects.filter(pk=pk,is_paid='no pagada').first()
    context={
        'order':order,
        'table':order.table,
        'categories':Category.objects.filter(type='vendible')
        }
    return render(request,'waiter/deliveryTable/order.html',context)

@login_required(login_url='admin/login/')
def list_orders_table_view(request,pk):
    shift=Shift.objects.filter(active=True).first()
    if shift is None:
        return redirect('/')
    table = Table.objects.filter(pk=pk).first()
    orders= table.order_set.filter(is_paid="no pagada").order_by('pk')
    context={
        'table':table,
        'orders':orders
    }
    return render(request,'waiter/deliveryTable/orders.html',context)

@login_required(login_url='admin/login/')
def list_orders_table_result_view(request,pk):
    table = Table.objects.filter(pk=pk).first()
    orders= table.order_set.filter(is_paid="no pagada").order_by('pk')
    context={
        'table':table,
        'orders':orders
    }
    return render(request,'waiter/deliveryTable/order_list_result.html',context)


@login_required(login_url='admin/login/')
def order_create_delivery_view(request,pk):
    if request.POST:
        table = Table.objects.filter(pk=pk).first()
        Order.objects.create(
            is_paid="no pagada",
            paid_method="efectivo",
            transfer = 0,
            cash = 0,
            shift = Shift.objects.filter(active=True).first(),
            table = table,
            user = request.user,
        )
        
        context={
            'orders':table.order_set.filter(is_paid='no pagada').order_by('pk'),
            'table':table,
            'categories': Category.objects.filter(type='vendible')
        }
        response= render(request,'waiter/deliveryTable/order_list_result.html',context)
        return response


@login_required(login_url='admin/login/')
def order_delivery_delete_view(request,pk):
    order = Order.objects.filter(pk=pk,is_paid='no pagada').first()
    context={}
    if request.POST:
        table=order.table
        order.delete()
        context['table']=table
        context['orders']=table.order_set.filter(is_paid='no pagada').order_by('pk')
        return render(request,'waiter/deliveryTable/order_list_result.html',context)
    context['order']=order
    return render(request,'waiter/deliveryTable/orderDelete/orderDeleteVerify.html',context)

@login_required(login_url='/admin/login/')
def order_change_table_delivery_form_view(request,pk):
    order = Order.objects.filter(pk=pk).first()
    context={'order':order}
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
            context['message']="Cambio de mesa realizado"
            response = HttpResponse()
            response["HX-Redirect"]= '/waiter/'
            return response
        else:
            context['error']="Mesa no disponible"
            
    context['tables']=Table.objects.filter(active=True,state="libre").order_by('id')
    response = render(request,'waiter/orderChangeTable/orderChangeTableForm.html',context)
    return response

@login_required(login_url='admin/login/')
def reload_order_sold_detail_delivery_table_view(request,pk):
    order = Order.objects.filter(pk=pk).first()
    context={
        'orders':order.table.order_set.filter(is_paid='no pagada'),
        'table':order.table,
        }
    print("entro aqui porque la tabla es de entreaga rapida")
    return render(request,'waiter/deliveryTable/order_list_result.html',context)


@login_required(login_url='/admin/login/')
def order_delivery_sold(request,pk):
    order = Order.objects.filter(pk=pk).first()
    context={
        "order":order
    }
    if request.method == "POST":
        data = order_paid_proccess_data(request.POST,order.total_price)
        form = CreateOrderSoldForm(data)
        if form.is_valid():
            order.paid_method= data['paid_method']
            order.is_paid="pagada"
            order.cash = data['cash']
            order.transfer = data['transfer']
            order.table.state="libre"
            order.save()
            order.table.save()
            for item in order.item_set.filter(state="entregado"):
                order.shift.add_revenue(item.revenue_price)
            context["message"]="Pago realizado con éxito"
        else:
            context["form"]=form
    response= render(request,'waiter/deliveryTable/orderSold/orderSoldVerify.html',context)
    return response

@login_required(login_url='/admin/login/')
def table_order_delivery_sold(request,pk):
    order = Order.objects.filter(pk=pk).first()
    context={
        "order":order
    }
    if request.method == "POST":
        data = order_paid_proccess_data(request.POST,order.total_price)
        form = CreateOrderSoldForm(data)
        if form.is_valid():
            order.paid_method= data['paid_method']
            order.is_paid="pagada"
            order.cash = data['cash']
            order.transfer = data['transfer']
            order.table.state="libre"
            order.save()
            order.table.save()
            for item in order.item_set.filter(state="entregado"):
                order.shift.add_revenue(item.revenue_price)
            context["message"]="Pago realizado con éxito"
        else:
            context["form"]=form
    response= render(request,'waiter/deliveryTable/TableOrdersSold/orderSoldVerify.html',context)
    return response

@login_required(login_url='admin/login/')
def charge_delivery_table(request,pk):
    table = Table.objects.filter(pk=pk,active=True).first()
    response = HttpResponse()
    response["HX-Redirect"]= f'/waiter/list_orders_table_view/{table.pk}'
    return response

@login_required(login_url='admin/login/')
def delivery_order_item_check_all_view(request,pk):
    order= Order.objects.filter(pk=pk,is_paid='no pagada').first()
    items = Item.objects.filter(order=order,is_active=False,state="ordenado")
    for item in items:
        item.is_active =True
        item.save()
    context={
        "order":order,
        
    }
    return render(request,'waiter/deliveryTable/order_item_list_result.html',context)

@login_required(login_url='admin/login/')
def delivery_order_item_revert_all_view(request,pk):
    order= Order.objects.filter(pk=pk,is_paid='no pagada').first()
    items = Item.objects.filter(order=order,is_active=True,state="ordenado")
    for item in items:
        item.is_active =False
        item.save()
    context={
        "order":order,
        
    }
    return render(request,'waiter/deliveryTable/order_item_list_result.html',context)