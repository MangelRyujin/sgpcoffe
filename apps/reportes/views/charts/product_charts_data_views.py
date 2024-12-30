from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.cuentas.models import CashOperation, Item, Operation,  Shift
from utils.validates.validate_date import validate_dates

@login_required(login_url='/admin/login/')
def product_statistics_view(request):
    if request.method == 'POST':
        start_date = request.POST.get('shift__in_date_after')
        end_date = request.POST.get('shift__in_date_before')
        validation_result, message = validate_dates(start_date, end_date)
        total_sales_amount=0
        if validation_result:
            shifts = Shift.objects.filter(in_date__gte=start_date, in_date__lte=end_date)
            items= Item.objects.filter(order__shift__in=shifts,order__is_paid='pagada',state__in=["entregado","cancelado"])
            products_sold = items.values('product__name','product__pk').annotate(cost_price=Sum('cost_price'),total_price=Sum('total_price'),total_count=Sum('cant'),revenue_price=Sum('revenue_price')).order_by('-total_count','-total_price')
            for item in items:
                if item.state == "cancelado":
                    pass
                else:
                    total_sales_amount+=item.total_price
            for product in products_sold:
                product['revenue_price'] = product['total_price']-product['cost_price']
            total_count = products_sold.aggregate(total_count=Sum('total_count'))['total_count'] or 0
            total_revenue_amount=sum(product['total_price'] - product['cost_price'] for product in products_sold) or 0
            total_cost_amount=products_sold.aggregate(total_cost_sum=Sum('cost_price'))['total_cost_sum'] or 0
            operations= Operation.objects.filter(operation_date__gte=start_date, operation_date__lte=end_date)
            cashOperations = CashOperation.objects.filter(shift__in=shifts)
            total_operation_amount_ingreso=0
            total_operation_amount_gasto=0
            total_operation_amount = 0
            total_cashOperation_amount_ingreso=0
            total_cashOperation_amount_gasto=0
            total_cashOperation_amount=0
            for operation in operations:
                total_operation_amount+=operation.amount
                if operation.operation_type == "ingreso":
                    total_operation_amount_ingreso+=operation.amount
                else:
                    total_operation_amount_gasto+=operation.amount
                
            for cashOperation in cashOperations:
                total_cashOperation_amount+=cashOperation.amount
                if cashOperation.operation_type == "ingreso":
                    total_cashOperation_amount_ingreso+=cashOperation.amount
                else:
                    total_cashOperation_amount_gasto+=cashOperation.amount
                    
            # Preparamos los datos para enviarlos a la plantilla
            context = {
                'products': products_sold,
                'total_price': total_sales_amount,
                'total_revenue':total_revenue_amount,
                'total_cost':total_cost_amount,
                'total_count':total_count,

                'total_operation_amount_ingreso':total_operation_amount_ingreso,
                'total_operation_amount_gasto':total_operation_amount_gasto,

                'total_cashOperation_amount_ingreso':total_cashOperation_amount_ingreso,
                'total_cashOperation_amount_gasto':total_cashOperation_amount_gasto,
                
                'ganancia_total':total_revenue_amount + total_cashOperation_amount_ingreso + total_operation_amount_ingreso - total_operation_amount_gasto - total_cashOperation_amount_gasto
                
            }
            return render(request, "charts/product_statistics.html", context)
        else:
            return render(request, "charts/product_statistics.html", {'message':message})
    else:
        # for item in Item.objects.all():
        #         item.cost_price = item.total_price - item.revenue_price
        #         item.save()
        return render(request, "charts/product_statistics.html", {})

  
