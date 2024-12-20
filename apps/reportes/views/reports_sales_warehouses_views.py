from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.cuentas.models import Item, Order
from apps.movimientos.models import StockMovements
from apps.productos.models import Stock
from utils.validates.validate_date import validate_dates
from apps.cuentas.order_filter import ItemStockFilter 

@login_required(login_url='/admin/login/')
def reports_sales_warehouses_view(request):
    stocks = Stock.objects.filter(stock_category__name="Consumibles").order_by('name')
    context={
        'stocks':stocks,
        'sum_cost':sum(stock.unit_price for stock in stocks) or 0,
        'total_cost':sum(stock.unit_price*stock.stock for stock in stocks) or 0,
        }
    
        
    return render(request, "reports_sales_warehouses/index.html", context)

@login_required(login_url='/admin/login/')
def reports_result_sales_warehouses_view(request):
    context={}
    if request.GET:
        request_get = request.GET.copy()
        items = ItemStockFilter(request.GET, queryset=Item.objects.all().order_by('-pk'))
        stock = Stock.objects.get(pk=request_get['stock'])or None
        stock_movements= StockMovements.objects.filter(stock=stock,created_date__lte=request_get['shift__in_date'])
        stock_total_movement = sum(mov.cant for mov in stock_movements if mov.type == "entrada") - sum(mov.cant for mov in stock_movements if mov.type == "salida")
        context['stock']=stock
        context['shift__in_date']=request_get['shift__in_date']
        context['stock_select']=request_get['stock']
        context['items']=items.qs
        context['stock_movements']=stock_movements
        context['stock_total_movement'] = stock_total_movement
        
    return render(request, "reports_sales_warehouses/result.html", context)