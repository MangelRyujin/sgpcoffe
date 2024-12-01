from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.cuentas.models import CashOperation, Item, Operation,  Shift
from utils.validates.validate_date import validate_dates
from django.db.models import Avg, OuterRef, Subquery, F
from datetime import timedelta


@login_required(login_url='/admin/login/')
def products_time_proccess(request):
    context={}
    if request.POST:
        start_date = request.POST.get('shift__in_date_after')
        end_date = request.POST.get('shift__in_date_before')
        context['start_date']=start_date
        context['end_date']=end_date
        validation_result, message = validate_dates(start_date, end_date)
        if message:
            context['error']=message
        if validation_result:
            shifts = Shift.objects.filter(in_date__gte=start_date, in_date__lte=end_date)
        #     items= Item.objects.filter(order__shift__in=shifts,order__is_paid='pagada',state__in=["entregado"])
        product_avg_time = Item.objects.filter(
                order__shift__in=shifts,
                order__is_paid='pagada',
                state='entregado'
            ).values('product__name','product__pk').annotate(total_count=Sum('cant'),
                avg_time=Avg(F("end_time")-F("created_time"))).order_by('product__name')
            # Agregar el resultado a la contexto
        for product in product_avg_time:
            if product['avg_time']:
                if product['avg_time'] > timedelta(minutes=20):
                    product['bg']="table-danger"
                elif product['avg_time'] > timedelta(minutes=15):
                    product['bg']="table-warning"
                else:
                    product['bg']="table-success"
            else:
                product['avg_time']= timedelta(seconds=0)
            
        context['products'] = product_avg_time
        print(product_avg_time)
    return render(request, "products_time_proccess/index.html", context)

  
