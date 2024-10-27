from django.http import JsonResponse
from django.shortcuts import render
from apps.cuentas.models import Order, Item
from apps.waiter.utils.generar_html_impresion import generar_html_impresion_funtion

# from utils.print.print2 import generar_html_impresion

def get_products_print(request,pk):
    order = Order.objects.filter(pk=pk).first()
    generar_html_impresion_funtion(order)
    return render(request,'waiter/print/printBTN.html')