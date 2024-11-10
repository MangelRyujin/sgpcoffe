from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.productos.models import Stock 

@login_required(login_url='admin/login/')
def home_view(request):
    return render(request,'index.html')


def notifications():
    stock= Stock.objects.all().order_by("stock")
    stock_in_danger=[s for s in stock if s.stock <= s.storage_threshold]
    context={
        "stock_in_danger":stock_in_danger
    }
    return context

@login_required(login_url='admin/login/')
def notification_view(request):
    return render(request,'notifications.html',context=notifications())

@login_required(login_url='admin/login/')
def notification_empty_view(request):
    return render(request,'notifications_icon.html',context=notifications())
