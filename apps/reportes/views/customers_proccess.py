from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.cuentas.models import CashOperation, Item, Operation, Order,  Shift
from apps.mesas.models import Table
from utils.validates.validate_date import validate_dates
from django.db.models import Avg, OuterRef, Subquery, F
from datetime import timedelta

def item_revenue():
    items = Item.objects.filter(state="cancelado")
    for item in items:
        item.total_price=0
        item.revenue_price=0
        item.save()
    
@login_required(login_url='/admin/login/')
def customers_proccess(request):
    item_revenue()
    context={}
    if request.POST:
        tables= Table.objects.filter(delivered=False).order_by('pk')
        start_date = request.POST.get('shift__in_date_after')
        end_date = request.POST.get('shift__in_date_before')
        context['start_date']=start_date
        context['end_date']=end_date
        validation_result, message = validate_dates(start_date, end_date)
        if message:
            context['error']=message
        if validation_result:
            shifts = Shift.objects.filter(in_date__gte=start_date, in_date__lte=end_date)
            tables_customers = tables.values('pk','name')
            for table in tables_customers:
                count = Order.objects.filter(shift__in=shifts,table=table['pk'],is_paid='pagada').count()
                table['cant'] = sum(order.customers for order in Order.objects.filter(shift__in=shifts,table=table['pk'],is_paid='pagada'))
                table['avg'] = table['cant']/count if count > 0 or table['cant'] > 0 else 0
        context['tables']=tables_customers    
    return render(request, "customers_proccess/index.html", context)


@login_required(login_url='/admin/login/')
def customers_proccess_charge_orders(request,pk,start_date,end_date):
    shifts = Shift.objects.filter(in_date__gte=start_date, in_date__lte=end_date)
    orders=Order.objects.filter(shift__in=shifts,table=pk,is_paid='pagada').order_by('pk')
    context={
        'orders':orders
    }
    return render(request, "customers_proccess/charge_orders.html",context)
