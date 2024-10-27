from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from apps.cuentas.models import AddItem, Item, Order, UtilsItem
from apps.productos.models import Category

@login_required(login_url='admin/login/')
def order_detail_delivery_delete_view(request,pk):
    order = Order.objects.filter(pk=pk).first()
    table=order.table
    if order.order_delete:
        order.delete()
    return redirect('list_orders_table_view',pk=table) 
   