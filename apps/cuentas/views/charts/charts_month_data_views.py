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
    shift = Shift.objects.filter(in_date__month=monthYear,in_date__year=month)
    grouped_shift = shift.annotate(day=TruncDay("in_date")).values("day","pk").order_by("day")
    sales_dict = {}
    for group in grouped_shift:
        shift= Shift.objects.get(pk =group["pk"])
        day_str = group["day"].strftime(f"{'%d'}")
        sales_dict[day_str] = shift.balance
    
    return JsonResponse({
        "title": f"Ventas por día en {month}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Total vendido",
                "backgroundColor": colorDanger,  
                "borderColor": colorDanger, 
                "data": list(sales_dict.values()),
            }]
        },
    })


@staff_member_required
def spend_month_per_customer_chart(request, month,monthYear):
    shift = Shift.objects.filter(in_date__month=monthYear,in_date__year=month)
    grouped_shift = shift.annotate(day=TruncDay("in_date")).values("day","pk").order_by("day")
    list_shift_total = get_month_dict()
    list_shift_transfer = get_month_dict()
    list_shift_cash = get_month_dict()
    for group in grouped_shift:
        day_of_week = days_of_week.get(calendar.day_name[group["day"].weekday()], 'Día desconocido')
        shift= Shift.objects.get(pk =group["pk"])
        day_str = group["day"].strftime(f"{'%d'}\n{day_of_week}")
        list_shift_total[day_str] = shift.balance
        list_shift_transfer[day_str] = shift.transferencia
        list_shift_cash[day_str] = shift.efectivo
    
    return JsonResponse({
        "title": f"Gasto por cliente por día en {month}",
        "data": {
            "labels": list(list_shift_total.keys()),
            "datasets": [{
                "label": "Total vendido",
                "backgroundColor": colorDanger,
                "borderColor": colorDanger,
                "data": list(list_shift_total.values()),
            },
                         {
                "label": "Transferencia",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(list_shift_transfer.values()),
            },
                         {
                "label": "Efectivo",
                "backgroundColor": colorSuccess,
                "borderColor": colorSuccess,
                "data": list(list_shift_cash.values()),
            }]
        },
    })

@staff_member_required
def payment_month_success_chart(request, month,monthYear):
    shifts = Shift.objects.filter(in_date__month=monthYear,in_date__year=month)
    total=0
    cash=0
    transfer=0
    for shift in shifts:
        total+=shift.balance
        cash+=shift.efectivo
        transfer+=shift.transferencia

    return JsonResponse({
        "title": f"Payment success rate in {month}",
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


