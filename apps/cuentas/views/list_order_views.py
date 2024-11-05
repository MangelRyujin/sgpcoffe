from django.shortcuts import render
from apps.cuentas.order_filter import OrderFilter 
from apps.cuentas.models import Order
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from apps.mesas.models import Table
from django.core.paginator import Paginator


@login_required(login_url='/admin/login/')
def order_view(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    users = User.objects.filter(is_superuser=False)
    tables = Table.objects.filter(active=True)
    if request.GET.get('message'):
        if get_copy['message'] == 'false':
            orders = OrderFilter(request.GET, queryset=Order.objects.filter(is_paid="pagada").order_by('-pk'))
        else:
            orders = OrderFilter(request.GET, queryset=Order.objects.filter(is_paid="pagada",item__message__isnull=False).exclude(
            item__message=''
        ).distinct().order_by('-pk'))
            
    else:   
        orders = OrderFilter(request.GET, queryset=Order.objects.filter(is_paid="pagada").order_by('-pk'))
    paginator = Paginator(orders.qs, 100 ) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={"orders":orders.qs,"users":users,"tables":tables,"pagination":page_obj,'parameters': parameters,} 
    return render(request,'order_list.html',context)

