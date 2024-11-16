from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.cuentas.models import Item,  Shift
from apps.movimientos.models import PrincipalStockMovements, StockMovements
from apps.productos.models import PrincipalStock, Stock
from utils.validates.validate_date import validate_dates

@login_required(login_url='/admin/login/')
def reports_warehouses_view(request):
    stocks= Stock.objects.filter(stock_category__name="Consumibles").annotate(total_cost=Sum('stock')*Sum('unit_price')).order_by('name')
    stocks2= PrincipalStock.objects.filter(stock_category__name="Consumibles").annotate(total_cost=Sum('stock')*Sum('unit_price')).order_by('name')
    context={
        'stocks':stocks,
        'stocks2':stocks2,
        'sum_cost':sum(stock.unit_price for stock in stocks) or 0,
        'total_cost':sum(stock.unit_price*stock.stock for stock in stocks) or 0,
        'sum_cost2':sum(stock.unit_price for stock in stocks2) or 0,
        'total_cost2':sum(stock.unit_price*stock.stock for stock in stocks2) or 0,
        
        }
    return render(request, "reports_warehouses/index.html", context)

  

@login_required(login_url='/admin/login/')
def reports_warehouses_stock_movement_view(request,pk):
    movements= StockMovements.objects.filter(stock=pk).order_by("pk")
    context={
        'movements':movements,
        }
    return render(request, "reports_warehouses/movement_list.html", context)

  

@login_required(login_url='/admin/login/')
def reports_warehouses_stock_principal_movement_view(request,pk):
    movements2= PrincipalStockMovements.objects.filter(stock=pk).order_by("pk")
    context={
        'movements2':movements2,
        }
    return render(request, "reports_warehouses/principal_movement_list.html", context)