from django.shortcuts import render
from apps.cuentas.order_filter import OrderFilter 
from apps.cuentas.models import AddItem, Item, Order, UtilsItem
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from apps.mesas.models import Table
from utils.product_validate.validate_ingredients_and_add_cant import validate_product_discount_ingredient
from django.db.models import Q


@login_required(login_url='/admin/login/')
def elaboration_items(request):
    return render(request,'items_bar_and_kitchen.html')


@login_required(login_url='/admin/login/')
def items_list_bar_view(request):

    bar=[]
    for item in Item.objects.filter(Q(state="ordenado") | Q(state="preparando"),product__place="bar").order_by('type'):
       bar.append({
           'bar':item,
           'add': AddItem.objects.filter(
                            item = item
                        ),
           'util': UtilsItem.objects.filter(
                            item = item
                        )
       })
    context ={"bars":bar} 
    return render(request,'items/items_bar.html',context)


@login_required(login_url='/admin/login/')
def items_list_kitchen_view(request):
    
    kitchen=[]
    for item in Item.objects.filter(Q(state="ordenado") | Q(state="preparando"),product__place="cocina").order_by('type'):
       kitchen.append({
           'kitchen':item,
           'add': AddItem.objects.filter(
                            item = item
                        ),
           'util': UtilsItem.objects.filter(
                            item = item
                        )
       })
    context ={"kitchens":kitchen} 
    return render(request,'items/items_kitchen.html',context)

