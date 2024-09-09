from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse

from apps.cuentas.models import CashOperation, Operation, Order,Shift
from utils.charts.chart import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict,colorPalette


@staff_member_required
def get_revenue_filter_options(request):
    grouped_purchases = Shift.objects.annotate(year=ExtractYear("in_date")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse({
        "options": options,
    })


@staff_member_required
def get_revenue_total_chart(request, year):
    shifts = Shift.objects.filter(in_date__year=year)
    grouped_shifts= shifts.annotate(month=ExtractMonth("in_date"))\
        .values("month","pk").order_by("month")
    operation = Operation.objects.filter(operation_date__year=year)
    grouped_operation= operation.annotate(month=ExtractMonth("operation_date"))\
        .values("month","pk").order_by("month")
    
    sales_dict = get_year_dict()
    for group in grouped_shifts:
        shift= Shift.objects.get(pk =group["pk"])
        sales_dict[months[group["month"]-1]]+= shift.revenue + shift.shift_total_operations
    for group in grouped_operation:
        operation= Operation.objects.get(pk =group["pk"])
        if operation.operation_type == "ingreso":
            sales_dict[months[group["month"]-1]]+= operation.amount
        else:
            sales_dict[months[group["month"]-1]]-= operation.amount
            
    return JsonResponse({
        "title": f"Ventas en {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Ganancia total",
                "backgroundColor": colorDanger,  # Asegúrate de definir esta variable
                "borderColor": colorDanger,  # Asegúrate de definir esta variable
                "data": list(sales_dict.values()),
            }]
        },
    })

@staff_member_required
def revenue_spend_per_customer_total_chart(request, year):
    shifts = Shift.objects.filter(in_date__year=year)
    grouped_shifts= shifts.annotate(month=ExtractMonth("in_date"))\
        .values("month","pk").order_by("month")
    operation = Operation.objects.filter(operation_date__year=year)
    grouped_operation= operation.annotate(month=ExtractMonth("operation_date"))\
        .values("month","pk").order_by("month")
    list_orders_total = get_year_dict()
    list_orders_transfer = get_year_dict()
    list_orders_cash = get_year_dict()
    for group in grouped_shifts:
        shift= Shift.objects.get(pk =group["pk"])
        list_orders_total[months[group["month"]-1]]+= shift.revenue + shift.shift_total_operations
    for group in grouped_operation:
        operation= Operation.objects.get(pk =group["pk"])
        if operation.operation_type == "ingreso":
            list_orders_total[months[group["month"]-1]]+= operation.amount
        else:
            list_orders_total[months[group["month"]-1]]-= operation.amount

    return JsonResponse({
        "title": f"Spend per customer in {year}",
        "data": {
            "labels": list(list_orders_total.keys()),
            "datasets": [{
                "label": "Ganancia total:",
                "backgroundColor": colorDanger,
                "borderColor": colorDanger,
                "data": list(list_orders_total.values()),
            }]
        },
    })


@staff_member_required
def revenue_payment_success_chart(request, year):
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

