from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse

from apps.cuentas.forms.item_form import OrderTableForm
from apps.cuentas.models import Item, Order
from apps.mesas.models import Table
from apps.productos.models import Category
from apps.waiter.order_forms import CreateOrderSoldForm
from apps.waiter.utils.order import order_paid_proccess_data

@login_required(login_url='admin/login/')
def order_detail_view(request,pk):
    order = Order.objects.filter(pk=pk,is_paid='no pagada').first()
    context={'order':order}
    return render(request,'waiter/orderDetail/orderDetail.html',context)

@login_required(login_url='admin/login/')
def example_view(request):
    tables = Table.objects.filter(active=True).order_by('id')
    context={}
    context['tables']=tables
    return render(request,'waiter/waiter.html',context)

@login_required(login_url='admin/login/')
def table_list_update_view(request):
    tables = Table.objects.filter(active=True).order_by('id')
    context={}
    context['tables']=tables
    return render(request,'waiter/tableList/table_list.html',context)

@login_required(login_url='admin/login/')
def charge_table(request,pk):
    table = Table.objects.filter(pk=pk,active=True).first()
    order= Order.objects.filter(table=table,is_paid='no pagada').first()
    context={
        "order":order,
        "table":table,
        'categories': Category.objects.filter(type='vendible')
    }
    return render(request,'waiter/table.html',context)

@login_required(login_url='admin/login/')
def order_items_result(request,pk):
    order= Order.objects.filter(pk=pk).first()
    context={
        "order":order,
    }
    
    return render(request,'waiter/itemsResult.html',context)

@login_required(login_url='/admin/login/')
def order_change_table_form_view(request,pk):
    order = Order.objects.filter(pk=pk).first()
    context={'order':order}
    response={}
    post=False
    affter_table=order.table
    if request.method == "POST":
        post=True
        table= Table.objects.get(id=request.POST.get("table"))
        if table.state == "libre":
            order.table.state="libre"
            order.table.save()
            order.table=table
            if table.delivered == False:
                table.state="ocupada"
                table.save()
            else:
              context['affter_table']=affter_table
            order.save()
            context['message']="Cambio de mesa realizado"
        else:
            context['error']="Mesa no disponible"
    context['tables']=Table.objects.filter(active=True,state="libre").order_by('id')
    response = render(request,'waiter/orderChangeTable/orderChangeTableForm.html',context)
    if post:
        response['HX-Trigger']='update-table-list' 
    return response


@login_required(login_url='/admin/login/')
def order_sold(request,pk):
    order = Order.objects.filter(pk=pk).first()
    context={
        "order":order
    }
    valid=False
    if request.method == "POST":
        data = order_paid_proccess_data(request.POST,order.total_price)
        form = CreateOrderSoldForm(data)
        if form.is_valid():
            valid=True
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
    response= render(request,'waiter/OrderSold/OrderSoldVerify.html',context)
    if valid:
        response['HX-Trigger']='update-table-list'
    return response