from django.shortcuts import render
from apps.cuentas.order_filter import OrderFilter 
from apps.cuentas.models import Order, Shift
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from apps.mesas.models import Table
from django.core.paginator import Paginator
from datetime import date,time

@login_required(login_url='/admin/login/')
def unpaid_order_view(request):
    if request.POST:
        table = Table.objects.get(pk=request.POST.get('table'))
        Order.objects.create(
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
        
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    users = User.objects.all()
    shift= Shift.objects.filter(active=True).first()
    tables = Table.objects.all()
    tables_form = Table.objects.filter(state="libre",active=True)
    orders = OrderFilter(request.GET, queryset=Order.objects.filter(is_paid="no pagada").order_by('-pk'))
    paginator = Paginator(orders.qs, 100 ) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={"orders":orders.qs,"users":users,"tables":tables,"pagination":page_obj,'parameters': parameters,"tables_form":tables_form,"shift":shift} 
    return render(request,'order_unpaid/unpaid_order_list.html',context)