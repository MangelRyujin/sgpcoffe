from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth,TruncDay
from django.http import JsonResponse
import calendar
from apps.cuentas.models import Item, Order,Shift
from apps.productos.models import Product
from utils.charts.chart import colorPrimary, colorSuccess, colorDanger,get_month_dict,days_of_week,get_product_month_dict


@staff_member_required
def get_filter_month_options(request):
    grouped_purchases = Shift.objects.annotate(year=ExtractYear("in_date")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]
    # Agrupa los productos por nombre y cuenta cuántas veces aparecen
    products = Product.objects.values('name').annotate(count=Count('name')).order_by('name')

    # Convierte los resultados en una lista de nombres de productos
    product_names = [product['name'] for product in products]

    return JsonResponse({
        "options": options,
        "products_month": product_names,
    })


@staff_member_required
def get_day_sales_chart(request, month,monthYear,monthproduct,monthproduct2,monthproduct3):

    
    items1 = Item.objects.filter(order__shift__in_date__month=monthYear,order__shift__in_date__year=month,order__is_paid='pagada',product__name=monthproduct)
    grouped_items = items1.annotate(day=TruncDay("order__shift__in_date"))\
        .values("day").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("day", "total_price","cant").order_by("day")
        
    items2 = Item.objects.filter(order__shift__in_date__month=monthYear,order__shift__in_date__year=month,order__is_paid='pagada',product__name=monthproduct2)
    grouped_items2 = items2.annotate(day=TruncDay("order__shift__in_date"))\
        .values("day").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("day", "total_price","cant").order_by("day")
        
    items3 = Item.objects.filter(order__shift__in_date__month=monthYear,order__shift__in_date__year=month,order__is_paid='pagada',product__name=monthproduct3)
    grouped_items3 = items3.annotate(day=TruncDay("order__shift__in_date"))\
        .values("day").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("day", "total_price","cant").order_by("day")
    
    
    days= get_product_month_dict(month,monthYear)
    sales_dict = get_product_month_dict(month,monthYear)
    sales_dict2 = get_product_month_dict(month,monthYear)
    sales_dict3 = get_product_month_dict(month,monthYear)
    
    for group in grouped_items:
        day_str = group["day"].strftime(f"{'%d'}")
        sales_dict[day_str] = group["cant"]
        
    for group2 in grouped_items2:
        day_str2 = group2["day"].strftime(f"{'%d'}")
        sales_dict2[day_str2] = group2["cant"]
        
    for group3 in grouped_items3:
        day_str3 = group3["day"].strftime(f"{'%d'}")
        sales_dict3[day_str3] = group3["cant"]
        
    day_copy = []
       
    for key,value in days.items():
        if sales_dict[key] == 0 and sales_dict2[key] == 0 and sales_dict3[key] == 0:
            del sales_dict[key]
            del sales_dict2[key]
            del sales_dict3[key]
        else:
            day_copy.append(key)
   
    return JsonResponse({
        "title": f"Ventas por día en {month}",
        "data": {
            "labels": day_copy,
            "datasets": [{
                "label": monthproduct,
                "backgroundColor": colorDanger,  # Asegúrate de definir esta variable
                "borderColor": colorDanger,  # Asegúrate de definir esta variable
                "data": list(sales_dict.values()),
            },
                         {
                "label": monthproduct2,
                "backgroundColor": colorPrimary,  # Asegúrate de definir esta variable
                "borderColor": colorPrimary,  # Asegúrate de definir esta variable
                "data": list(sales_dict2.values()),
            },
                         {
                "label": monthproduct3,
                "backgroundColor": colorSuccess,  # Asegúrate de definir esta variable
                "borderColor": colorSuccess,  # Asegúrate de definir esta variable
                "data": list(sales_dict3.values()),
            }]
        },
    })


@staff_member_required
def spend_month_per_customer_chart(request, month,monthYear,monthproduct,monthproduct2,monthproduct3):
    items1 = Item.objects.filter(order__shift__in_date__month=monthYear,order__shift__in_date__year=month,order__is_paid='pagada',product__name=monthproduct)
    grouped_items = items1.annotate(day=TruncDay("order__shift__in_date"))\
        .values("day").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("day", "total_price","cant").order_by("day")
        
    items2 = Item.objects.filter(order__shift__in_date__month=monthYear,order__shift__in_date__year=month,order__is_paid='pagada',product__name=monthproduct2)
    grouped_items2 = items2.annotate(day=TruncDay("order__shift__in_date"))\
        .values("day").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("day", "total_price","cant").order_by("day")
        
    items3 = Item.objects.filter(order__shift__in_date__month=monthYear,order__shift__in_date__year=month,order__is_paid='pagada',product__name=monthproduct3)
    grouped_items3 = items3.annotate(day=TruncDay("order__shift__in_date"))\
        .values("day").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("day", "total_price","cant").order_by("day")
    
    
    days= get_product_month_dict(month,monthYear)
    sales_dict = get_product_month_dict(month,monthYear)
    sales_dict2 = get_product_month_dict(month,monthYear)
    sales_dict3 = get_product_month_dict(month,monthYear)
    
    for group in grouped_items:
        day_str = group["day"].strftime(f"{'%d'}")
        sales_dict[day_str] = group["cant"]
        
    for group2 in grouped_items2:
        day_str2 = group2["day"].strftime(f"{'%d'}")
        sales_dict2[day_str2] = group2["cant"]
        
    for group3 in grouped_items3:
        day_str3 = group3["day"].strftime(f"{'%d'}")
        sales_dict3[day_str3] = group3["cant"]
        
    day_copy = []
       
    for key,value in days.items():
        if sales_dict[key] == 0 and sales_dict2[key] == 0 and sales_dict3[key] == 0:
            del sales_dict[key]
            del sales_dict2[key]
            del sales_dict3[key]
        else:
            day_copy.append(key)
            
    return JsonResponse({
        "title": f"Gasto por cliente por día en {month}",
        "data": {
            "labels": day_copy,
            "datasets": [{
                "label": monthproduct,
                "backgroundColor": colorDanger,
                "borderColor": colorDanger,
                "data": list(sales_dict.values()),
            },
                         {
                "label": monthproduct2,
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(sales_dict2.values()),
            },
                         {
                "label": monthproduct3,
                "backgroundColor": colorSuccess,
                "borderColor": colorSuccess,
                "data": list(sales_dict3.values()),
            }]
        },
    })

@staff_member_required
def payment_month_success_chart(request, month,monthYear,monthproduct,monthproduct2,monthproduct3):
    items1 = Item.objects.filter(order__shift__in_date__month=monthYear,order__shift__in_date__year=month,order__is_paid='pagada',product__name=monthproduct)
    grouped_items = items1.aggregate(total=Sum('cant'))["total"] or 0
        
    items2 = Item.objects.filter(order__shift__in_date__month=monthYear,order__shift__in_date__year=month,order__is_paid='pagada',product__name=monthproduct2)
    grouped_items2 = items2.aggregate(total=Sum('cant'))["total"] or 0
        
    items3 = Item.objects.filter(order__shift__in_date__month=monthYear,order__shift__in_date__year=month,order__is_paid='pagada',product__name=monthproduct3)
    grouped_items3 = items3.aggregate(total=Sum('cant'))["total"] or 0
    print(grouped_items3)
    
    return JsonResponse({
        "title": f"Payment success rate in {month}",
        "data": {
            "labels": [monthproduct, monthproduct2,monthproduct3],
            "datasets": [{
                "label": "Total vendido",
                "backgroundColor": [colorDanger,colorPrimary, colorSuccess],
                "borderColor": [colorDanger,colorPrimary, colorSuccess],
                "data": [
                    grouped_items,
                    grouped_items2,
                    grouped_items3
                ],
            }]
        },
    })


