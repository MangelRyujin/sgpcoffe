from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse

from apps.cuentas.models import Order
from utils.charts.chart import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict,colorPalette


@staff_member_required
def get_filter_options(request):
    grouped_purchases = Order.objects.annotate(year=ExtractYear("created_date")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse({
        "options": options,
    })


@staff_member_required
def get_sales_chart(request, year):
    # Filtrar los pedidos por año
    orders = Order.objects.filter(created_date__year=year,is_paid='pagada')
    
    # Agrupar los pedidos por mes y calcular el total vendido
    grouped_orders = orders.annotate(total=F('transfer')+F('cash')).annotate(month=ExtractMonth("created_date"))\
       .values("month").annotate(average=Sum("transfer")+Sum("cash")).values("month", "average").order_by("month")
    
    sales_dict = {}
    for group in grouped_orders:
        sales_dict[months[group["month"]-1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Ventas en {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Total vendido por mes",
                "backgroundColor": colorPrimary,  # Asegúrate de definir esta variable
                "borderColor": colorPrimary,  # Asegúrate de definir esta variable
                "data": list(sales_dict.values()),
            }]
        },
    })


@staff_member_required
def spend_per_customer_chart(request, year):
    purchases = Order.objects.filter(created_date__year=year,is_paid='pagada')
    grouped_purchases = purchases.annotate(price=F("transfer")+F("cash")).annotate(month=ExtractMonth("created_date"))\
        .values("month").annotate(average=Sum("transfer")+Sum("cash")).values("month", "average").order_by("month")

    spend_per_customer_dict = get_year_dict()

    for group in grouped_purchases:
        spend_per_customer_dict[months[group["month"]-1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Spend per customer in {year}",
        "data": {
            "labels": list(spend_per_customer_dict.keys()),
            "datasets": [{
                "label": "Total vendido por mes:",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(spend_per_customer_dict.values()),
            }]
        },
    })


@staff_member_required
def payment_success_chart(request, year):
    purchases = Order.objects.filter(created_date__year=year,is_paid='pagada')
    bolth = purchases.filter(paid_method='ambos').aggregate(total=Sum('transfer')+Sum('cash'))['total'] or 0
    transfers_sum = purchases.filter(paid_method='transferencia').aggregate(total=Sum('transfer'))['total'] or 0
    cash_sum = purchases.filter(paid_method='efectivo').aggregate(total=Sum('cash'))['total'] or 0

    return JsonResponse({
        "title": f"Payment success rate in {year}",
        "data": {
            "labels": ["Transferencia", "Efectivo","Ambos"],
            "datasets": [{
                "label": "Amount ($)",
                "backgroundColor": [colorPrimary,colorSuccess, colorDanger],
                "borderColor": [colorPrimary,colorSuccess, colorDanger],
                "data": [
                    # purchases.filter(paid_method='transferencia').count(),
                    # purchases.filter(paid_method='efectivo').count(),
                    # purchases.filter(paid_method='ambos').count(),
                    transfers_sum,
                    cash_sum,
                    bolth,
                ],
            }]
        },
    })


@staff_member_required
def payment_method_chart(request, year):
    purchases = Order.objects.filter(created_date__year=year)
    grouped_purchases = purchases.values("paid_method").annotate(total=Sum('transfer')+Sum('cash'))\
        .values("paid_method", "total").order_by("paid_method")

    payment_method_dict = dict()

    for payment_method in Order.PAID_METHODS_CHOICES:
        payment_method_dict[payment_method[1]] = 0

    for group in grouped_purchases:
        payment_method_dict[dict(Order.PAID_METHODS_CHOICES)[group["paid_method"]]] = group["total"]

    return JsonResponse({
        "title": f"Payment method rate in {year}",
        "data": {
            "labels": list(payment_method_dict.keys()),
            "datasets": [{
                "label": "Monto total del año",
                "backgroundColor": generate_color_palette(len(payment_method_dict)),
                "borderColor": generate_color_palette(len(payment_method_dict)),
                "data": list(payment_method_dict.values()),
            }]
        },
    })