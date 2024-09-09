from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth,TruncDay
from django.http import JsonResponse
import calendar
from apps.cuentas.models import Operation, Order,Shift
from utils.charts.chart import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict,colorPalette,get_month_dict,days_of_week



@staff_member_required
def get_month_filter_options(request):
    grouped_purchases = Shift.objects.annotate(year=ExtractYear('in_date')).values('year').order_by('-year').distinct()
    options = [purchase['year'] for purchase in grouped_purchases]

    
    return JsonResponse({
        "options": options,
    })

@staff_member_required
def get_revenue_day_sales_chart(request, month,monthYear):
    shift = Shift.objects.filter(in_date__month=monthYear,in_date__year=month)
    
    grouped_shift = shift.annotate(day=TruncDay("in_date")).values("day","pk").order_by("day")
    sales_dict = {}
    for group in grouped_shift:
        shift= Shift.objects.get(pk =group["pk"])
        day_str = group["day"].strftime(f"{'%d'}")
        sales_dict[day_str] = shift.revenue
    
    return JsonResponse({
        "title": f"Ventas por día en {month}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Total de venta",
                "backgroundColor": colorDanger,  
                "borderColor": colorDanger, 
                "data": list(sales_dict.values()),
            }]
        },
    })


@staff_member_required
def revenue_spend_month_per_customer_chart(request, month,monthYear):
    shift = Shift.objects.filter(in_date__month=monthYear,in_date__year=month)
    grouped_shift = shift.annotate(day=TruncDay("in_date")).values("day","pk").order_by("day")
    list_shift_total = get_month_dict()
    for group in grouped_shift:
        shift= Shift.objects.get(pk =group["pk"])
        day_str = group["day"].strftime(f"{'%d'}")
        list_shift_total[day_str] = shift.revenue
    
    return JsonResponse({
        "title": f"Gasto por cliente por día en {month}",
        "data": {
            "labels": list(list_shift_total.keys()),
            "datasets": [{
                "label": "Total de venta",
                "backgroundColor": colorDanger,
                "borderColor": colorDanger,
                "data": list(list_shift_total.values()),
            }]
        },
    })
