from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth,TruncDay
from django.http import JsonResponse
import calendar
from apps.cuentas.models import Order,Shift
from utils.charts.chart import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict,colorPalette,get_month_dict,days_of_week



@staff_member_required
def get_month_filter_options(request):
    grouped_purchases = Shift.objects.annotate(year=ExtractYear('in_date')).values('year').order_by('-year').distinct()
    options = [purchase['year'] for purchase in grouped_purchases]

    return JsonResponse({
        "options": options,
    })

@staff_member_required
def get_day_sales_chart(request, month,monthYear):

    # Filtrar los pedidos por año
    orders = Order.objects.filter(shift__in_date__month=monthYear,shift__in_date__year=month, is_paid='pagada')
    
    # Agrupar los pedidos por día y calcular el total vendido
    grouped_orders = orders.annotate(day=TruncDay("shift__in_date")).values("day").annotate(total=Sum(F('transfer')+F('cash'))).order_by("day")
    
    
    
    sales_dict = {}
    for group in grouped_orders:
        day_str = group["day"].strftime(f"{'%d'}")
        sales_dict[day_str] = round(group["total"], 2)

    return JsonResponse({
        "title": f"Ventas por día en {month}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Total vendido",
                "backgroundColor": colorDanger,  # Asegúrate de definir esta variable
                "borderColor": colorDanger,  # Asegúrate de definir esta variable
                "data": list(sales_dict.values()),
            }]
        },
    })


@staff_member_required
def spend_month_per_customer_chart(request, month,monthYear):
    orders = Order.objects.filter(shift__in_date__month=monthYear,shift__in_date__year=month, is_paid='pagada')
    orders_total = orders.annotate(day=TruncDay("shift__in_date")).values("day").annotate(total=Sum(F("transfer")+F("cash")),transfer=Sum(F("transfer")),cash=Sum(F("cash"))).order_by("day")

    list_orders_total = get_month_dict()
    list_orders_transfer = get_month_dict()
    list_orders_cash = get_month_dict()
    
    for group in orders_total:
        day_of_week = days_of_week.get(calendar.day_name[group["day"].weekday()], 'Día desconocido')
        day_str = group["day"].strftime(f"{'%d'}\n{day_of_week}")
        list_orders_total[day_str] = round(group["total"], 2)
        list_orders_transfer[day_str] = round(group["transfer"], 2)
        list_orders_cash[day_str] = round(group["cash"], 2)
        
    return JsonResponse({
        "title": f"Gasto por cliente por día en {month}",
        "data": {
            "labels": list(list_orders_total.keys()),
            "datasets": [{
                "label": "Total vendido",
                "backgroundColor": colorDanger,
                "borderColor": colorDanger,
                "data": list(list_orders_total.values()),
            },
                         {
                "label": "Transferencia",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(list_orders_transfer.values()),
            },
                         {
                "label": "Efectivo",
                "backgroundColor": colorSuccess,
                "borderColor": colorSuccess,
                "data": list(list_orders_cash.values()),
            }]
        },
    })

@staff_member_required
def payment_month_success_chart(request, month,monthYear):
    purchases = Order.objects.filter(shift__in_date__month=monthYear,shift__in_date__year=month,is_paid='pagada')
    total = purchases.aggregate(total=Sum('transfer')+Sum('cash'))['total'] or 0
    transfers_sum = purchases.aggregate(total=Sum('transfer'))['total'] or 0
    cash_sum = purchases.aggregate(total=Sum('cash'))['total'] or 0

    return JsonResponse({
        "title": f"Payment success rate in {month}",
        "data": {
            "labels": ["Transferencia", "Efectivo","Total vendido"],
            "datasets": [{
                "label": "Total",
                "backgroundColor": [colorPrimary,colorSuccess, colorDanger],
                "borderColor": [colorPrimary,colorSuccess, colorDanger],
                "data": [
                    transfers_sum,
                    cash_sum,
                    total,
                ],
            }]
        },
    })


