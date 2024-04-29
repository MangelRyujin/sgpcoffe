from django.shortcuts import render

from apps.cuentas.models import Order


def order_view(request):
    objetos = Order.objects.all()
    return render(request,'order_list.html',{'objetos': objetos})