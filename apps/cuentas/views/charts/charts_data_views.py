from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse

from apps.cuentas.models import Order,Shift
from utils.charts.chart import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict,colorPalette


@staff_member_required
def get_filter_options(request):
    grouped_purchases = Shift.objects.annotate(year=ExtractYear("in_date")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse({
        "options": options,
    })


@staff_member_required
def get_sales_chart(request, year):
    # Filtrar los pedidos por año
    orders = Order.objects.filter(shift__in_date__year=year,is_paid='pagada')
    # Agrupar los pedidos por mes y calcular el total vendido
    grouped_orders = orders.annotate(month=ExtractMonth("shift__in_date"))\
       .values("month").annotate(total=Sum("transfer")+Sum("cash"),transfer=Sum(F("transfer")),cash=Sum(F("cash"))).values("month", "total","transfer","cash").order_by("month")
    
    sales_dict = {}
    transfer_dict = {}
    cash_dict = {}
    for group in grouped_orders:
        sales_dict[months[group["month"]-1]] = round(group["total"], 2)
        transfer_dict[months[group["month"]-1]] = round(group["transfer"], 2)
        cash_dict[months[group["month"]-1]] = round(group["cash"], 2)

    return JsonResponse({
        "title": f"Ventas en {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Total vendido",
                "backgroundColor": colorDanger,  # Asegúrate de definir esta variable
                "borderColor": colorDanger,  # Asegúrate de definir esta variable
                "data": list(sales_dict.values()),
            },
                         {
                "label": "Transferencia",
                "backgroundColor": colorPrimary,  # Asegúrate de definir esta variable
                "borderColor": colorPrimary,  # Asegúrate de definir esta variable
                "data": list(transfer_dict.values()),
            },
                         {
                "label": "Efectivo",
                "backgroundColor": colorSuccess,  # Asegúrate de definir esta variable
                "borderColor": colorSuccess,  # Asegúrate de definir esta variable
                "data": list(cash_dict.values()),
            }]
        },
    })


@staff_member_required
def spend_per_customer_chart(request, year):
    purchases = Order.objects.filter(shift__in_date__year=year,is_paid='pagada')
    grouped_purchases = purchases.annotate(price=F("transfer")+F("cash")).annotate(month=ExtractMonth("shift__in_date"))\
        .values("month").annotate(total=Sum("transfer")+Sum("cash"),transfer=Sum("transfer"),cash=Sum("cash")).values("month", "total","transfer","cash").order_by("month")

    list_orders_total = get_year_dict()
    list_orders_transfer = get_year_dict()
    list_orders_cash = get_year_dict()

    for group in grouped_purchases:
        list_orders_total[months[group["month"]-1]] = round(group["total"], 2)
        list_orders_transfer[months[group["month"]-1]] = round(group["transfer"], 2)
        list_orders_cash[months[group["month"]-1]] = round(group["cash"], 2)
    

    return JsonResponse({
        "title": f"Spend per customer in {year}",
        "data": {
            "labels": list(list_orders_total.keys()),
            "datasets": [{
                "label": "Total vendido:",
                "backgroundColor": colorDanger,
                "borderColor": colorDanger,
                "data": list(list_orders_total.values()),
            },{
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
def payment_success_chart(request, year):
    purchases = Order.objects.filter(shift__in_date__year=year,is_paid='pagada')
    total = purchases.aggregate(total=Sum('transfer')+Sum('cash'))['total'] or 0
    transfers_sum = purchases.aggregate(total=Sum('transfer'))['total'] or 0
    cash_sum = purchases.aggregate(total=Sum('cash'))['total'] or 0

    return JsonResponse({
        "title": f"Payment success rate in {year}",
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

