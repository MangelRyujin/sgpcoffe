from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.cuentas.models import Item,  Shift
from utils.validates.validate_date import validate_dates

@login_required(login_url='/admin/login/')
def product_statistics_view(request):
    if request.method == 'POST':
        start_date = request.POST.get('shift__in_date_after')
        end_date = request.POST.get('shift__in_date_before')
        validation_result, message = validate_dates(start_date, end_date)
        if validation_result:
            # Filtramos los turnos por el rango de fechas proporcionado
            shifts = Shift.objects.filter(in_date__gte=start_date, in_date__lte=end_date)
            items= Item.objects.filter(order__shift__in=shifts,order__is_paid='pagada')
            products_sold = items.values('product__name').annotate(total_price=Sum('total_price'),total_count=Sum('cant')).order_by('-total_count','-total_price')
            total_sales_amount = products_sold.aggregate(total_sales_sum=Sum('total_price'))['total_sales_sum']
            
            # Preparamos los datos para enviarlos a la plantilla
            context = {
                'products': products_sold,
                'total_price': total_sales_amount,
                
            }
            print(products_sold)
            return render(request, "charts/product_statistics.html", context)
        else:
            return render(request, "charts/product_statistics.html", {'message':message})
    else:
        return render(request, "charts/product_statistics.html", {})

  
