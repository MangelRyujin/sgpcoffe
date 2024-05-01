from django.shortcuts import render
from apps.cuentas.order_filter import OrderFilter 
from apps.cuentas.models import Order
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from apps.mesas.models import Table


@login_required(login_url='/admin/login/')
def order_view(request):
    users = User.objects.filter(is_superuser=False)
    tables = Table.objects.all()
    orders = OrderFilter(request.GET, queryset=Order.objects.filter(is_paid="pagada").order_by('pk'))
    context ={"orders":orders.qs,"users":users,"tables":tables} 
    return render(request,'order_list.html',context)