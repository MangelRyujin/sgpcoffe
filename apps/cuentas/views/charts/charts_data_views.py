from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse

from apps.cuentas.models import CashOperation, Order,Shift
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
    shifts = Shift.objects.filter(in_date__year=year)
    grouped_shifts= shifts.annotate(month=ExtractMonth("in_date"))\
        .values("month","pk").order_by("month")
    sales_dict = get_year_dict()
    transfer_dict = get_year_dict()
    cash_dict = get_year_dict()
    for group in grouped_shifts:
        shift= Shift.objects.get(pk =group["pk"])
        sales_dict[months[group["month"]-1]]+= shift.balance
        transfer_dict[months[group["month"]-1]]+= shift.transferencia
        cash_dict[months[group["month"]-1]]+= shift.efectivo

    return JsonResponse({
        "title": f"Ventas en {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Total",
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
    shifts = Shift.objects.filter(in_date__year=year)
    grouped_shifts= shifts.annotate(month=ExtractMonth("in_date"))\
        .values("month","pk").order_by("month")
    list_orders_total = get_year_dict()
    list_orders_transfer = get_year_dict()
    list_orders_cash = get_year_dict()
    for group in grouped_shifts:
        shift= Shift.objects.get(pk =group["pk"])
        list_orders_total[months[group["month"]-1]]+= shift.balance
        list_orders_transfer[months[group["month"]-1]]+= shift.transferencia
        list_orders_cash[months[group["month"]-1]]+= shift.efectivo

    return JsonResponse({
        "title": f"Spend per customer in {year}",
        "data": {
            "labels": list(list_orders_total.keys()),
            "datasets": [{
                "label": "Total:",
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
    shift = Shift.objects.filter(in_date__year=year)
    total=0
    cash=0
    transfer=0
    for s in shift:
        total+=s.balance
        cash+=s.efectivo
        transfer+=s.transferencia

    return JsonResponse({
        "title": f"Payment success rate in {year}",
        "data": {
            "labels": ["Transferencia", "Efectivo","Total"],
            "datasets": [{
                "label": "Total",
                "backgroundColor": [colorPrimary,colorSuccess, colorDanger],
                "borderColor": [colorPrimary,colorSuccess, colorDanger],
                "data": [
                    transfer,
                    cash,
                    total,
                ],
            }]
        },
    })

