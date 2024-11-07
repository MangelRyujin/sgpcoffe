from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse

from apps.cuentas.models import Item, Order,Shift
from apps.productos.models import Product
from utils.charts.chart import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict,colorPalette


@staff_member_required
def get_filter_options(request):
    grouped_purchases = Shift.objects.annotate(year=ExtractYear("in_date")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]
    # Agrupa los productos por nombre y cuenta cuántas veces aparecen
    products = Product.objects.values('name').annotate(count=Count('name')).order_by('name')

    # Convierte los resultados en una lista de nombres de productos
    product_names = [product['name'] for product in products]

    return JsonResponse({
        "options": options,
        "products": product_names,
    })


@staff_member_required
def get_product_sales_chart(request, year,product,product2,product3):
    # Filtrar los pedidos por año
    items1 = Item.objects.filter(order__shift__in_date__year=year,order__is_paid='pagada',product__name=product)
    grouped_items = items1.annotate(month=ExtractMonth("order__shift__in_date"))\
        .values("month").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("month", "total_price","cant").order_by("month")
    
    items2 = Item.objects.filter(order__shift__in_date__year=year,order__is_paid='pagada',product__name=product2)
    grouped_items2 = items2.annotate(month=ExtractMonth("order__shift__in_date"))\
        .values("month").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("month", "total_price","cant").order_by("month")
    
    items3 = Item.objects.filter(order__shift__in_date__year=year,order__is_paid='pagada',product__name=product3)
    grouped_items3 = items3.annotate(month=ExtractMonth("order__shift__in_date"))\
        .values("month").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("month", "total_price","cant").order_by("month")
        
    product1_dict = get_year_dict()
    product2_dict = get_year_dict()
    product3_dict = get_year_dict()
    for group in grouped_items:
        product1_dict[months[group["month"]-1]] = group["cant"]
        
    for group in grouped_items2:
        product2_dict[months[group["month"]-1]] = group["cant"]
        
    for group in grouped_items3:
        product3_dict[months[group["month"]-1]] = group["cant"]
        

    return JsonResponse({
        "title": f"Ventas en {year}",
        "data": {
            "labels": list(product1_dict.keys()),
            "datasets": [{
                "label":    product,
                "backgroundColor": colorDanger,  # Asegúrate de definir esta variable
                "borderColor": colorDanger,  # Asegúrate de definir esta variable
                "data": list(product1_dict.values()),
            },{
                "label":    product2,
                "backgroundColor":colorPrimary,  # Asegúrate de definir esta variable
                "borderColor": colorPrimary,  # Asegúrate de definir esta variable
                "data": list(product2_dict.values()),
            },{
                "label":    product3,
                "backgroundColor": colorSuccess,  # Asegúrate de definir esta variable
                "borderColor": colorSuccess,  # Asegúrate de definir esta variable
                "data": list(product3_dict.values()),
            }]
        },
    })


@staff_member_required
def spend_product_per_customer_chart(request, year,product,product2,product3):
    # Filtrar los pedidos por año
    items1 = Item.objects.filter(order__shift__in_date__year=year,order__is_paid='pagada',product__name=product)
    grouped_items = items1.annotate(month=ExtractMonth("order__shift__in_date"))\
        .values("month").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("month", "total_price","cant").order_by("month")
    
    items2 = Item.objects.filter(order__shift__in_date__year=year,order__is_paid='pagada',product__name=product2)
    grouped_items2 = items2.annotate(month=ExtractMonth("order__shift__in_date"))\
        .values("month").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("month", "total_price","cant").order_by("month")
    
    items3 = Item.objects.filter(order__shift__in_date__year=year,order__is_paid='pagada',product__name=product3)
    grouped_items3 = items3.annotate(month=ExtractMonth("order__shift__in_date"))\
        .values("month").annotate(total_price=Sum("total_price"),cant=Sum('cant')).values("month", "total_price","cant").order_by("month")
        
    product1_dict = get_year_dict()
    product2_dict = get_year_dict()
    product3_dict = get_year_dict()
    for group in grouped_items:
        product1_dict[months[group["month"]-1]] = group["cant"]
        
    for group in grouped_items2:
        product2_dict[months[group["month"]-1]] = group["cant"]
        
    for group in grouped_items3:
        product3_dict[months[group["month"]-1]] = group["cant"]
        
        
    return JsonResponse({
        "title": f"Ventas en {year}",
        "data": {
            "labels": list(product1_dict.keys()),
            "datasets": [{
                "label":    product,
                "backgroundColor": colorDanger,  # Asegúrate de definir esta variable
                "borderColor": colorDanger,  # Asegúrate de definir esta variable
                "data": list(product1_dict.values()),
            },{
                "label":    product2,
                "backgroundColor":colorPrimary,  # Asegúrate de definir esta variable
                "borderColor": colorPrimary,  # Asegúrate de definir esta variable
                "data": list(product2_dict.values()),
            },{
                "label":    product3,
                "backgroundColor": colorSuccess,  # Asegúrate de definir esta variable
                "borderColor": colorSuccess,  # Asegúrate de definir esta variable
                "data": list(product3_dict.values()),
            }]
        },
    })

@staff_member_required
def payment_product_success_chart(request, year,product,product2,product3):
    items1 = Item.objects.filter(order__shift__in_date__year=year,order__is_paid='pagada',product__name=product)
    grouped_items = items1.aggregate(cant=Sum('cant'))['cant'] or 0
    
    items2 = Item.objects.filter(order__shift__in_date__year=year,order__is_paid='pagada',product__name=product2)
    grouped_items2 = items2.aggregate(cant=Sum('cant'))['cant'] or 0
    
    items3 = Item.objects.filter(order__shift__in_date__year=year,order__is_paid='pagada',product__name=product3)
    grouped_items3 = items3.aggregate(cant=Sum('cant'))['cant'] or 0
    
    return JsonResponse({
        "title": f"Payment success rate in {year}",
        "data": {
            "labels": [product, product2,product3],
            "datasets": [{
                "label": "Total",
                "backgroundColor": [colorDanger,colorPrimary, colorSuccess],
                "borderColor": [colorDanger,colorPrimary, colorSuccess],
                "data": [
                    grouped_items,
                    grouped_items2,
                    grouped_items3,
                ],
            }]
        },
    })

