from django.shortcuts import render
from apps.cuentas.order_filter import OrderFilter 
from apps.cuentas.models import AddItem, Item, Order, UtilsItem
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from apps.mesas.models import Table
from utils.product_validate.validate_ingredients_and_add_cant import validate_product_discount_ingredient
from django.db.models import Q


def charge_items():
    context ={
        "bars":charge_bar_items(),
        "kitchens":charge_kitchen_items(),
        "bars_success":charge_bar_success_items(),
        "kitchens_success":charge_kitchen_success_items(),
        } 
    return context

def charge_bar_items():
    bar=[]
    for item in Item.objects.filter(Q(state="ordenado"),product__place="bar", is_active=True).order_by('-order__table__delivered','type','id'):
       bar.append({
           'bar':item,
           'add': AddItem.objects.filter(
                            item = item
                        ),
           'util': UtilsItem.objects.filter(
                            item = item
                        )
       })
    
    return bar

def charge_kitchen_items():
    kitchen=[]
    for item in Item.objects.filter(Q(state="ordenado"),product__place="cocina", is_active=True).order_by('-order__table__delivered','type','id'):
       kitchen.append({
           'kitchen':item,
           'add': AddItem.objects.filter(
                            item = item
                        ),
           'util': UtilsItem.objects.filter(
                            item = item
                        )
       })
    return kitchen

def charge_bar_success_items():
    bar_success=[]
    for item in Item.objects.filter(Q(state="preparando"),product__place="bar", is_active=True).order_by('-order__table__delivered','type','id'):
       bar_success.append({
           'bar':item,
           'add': AddItem.objects.filter(
                            item = item
                        ),
           'util': UtilsItem.objects.filter(
                            item = item
                        )
       })
    return bar_success

def charge_kitchen_success_items():
    kitchen_success=[]
    for item in Item.objects.filter(Q(state="preparando"),product__place="cocina", is_active=True).order_by('-order__table__delivered','type','id'):
       kitchen_success.append({
           'kitchen':item,
           'add': AddItem.objects.filter(
                            item = item
                        ),
           'util': UtilsItem.objects.filter(
                            item = item
                        )
       })
    return kitchen_success