from datetime import timezone
from django.shortcuts import render
from apps.barandkitchen.utils.items import all_charge_bar_items
from apps.cuentas.models import AddItem, Item, UtilsItem
from django.contrib.auth.decorators import login_required
from datetime import datetime
from apps.productos.models import ProductAddRelation
from utils.product_validate.validate_ingredients_and_add_cant import validate_product_discount_ingredient 


@login_required(login_url='/admin/login/')
def bar_elaboration_items(request):
    return render(request,'bar_and_kitchen/items_bar_proccess.html',context=all_charge_bar_items())

@login_required(login_url='/admin/login/')
def bar_ordenado(request):
    return render(request,'bar_and_kitchen/items/items_bar.html',context=all_charge_bar_items())

@login_required(login_url='/admin/login/')
def items_bar_proccess_view(request,pk):
    error=""
    if request.POST:
        item = Item.objects.filter(pk=pk,state="ordenado",is_active=True).first()
        error = validate_product_discount_ingredient(item)
        if error == '':
            item.total_price=item.estimate_price
            item.revenue_price=item.revenue
            item.cost_price = item.inversion_cost
            item.product.discount_ingredients(item.cant)
            for add in AddItem.objects.filter(item=item):
                product_add = ProductAddRelation.objects.get(add=add.add.id,product=item.product.id)
                product_add.discount_add(item.cant,add.cant)
            for util in UtilsItem.objects.filter(item=item):
                util.discount_util()
            item.state = "preparando"
            item.save()
    context=all_charge_bar_items()
    context['error']=error
    return render(request,'bar_and_kitchen/items/items_bar.html',context)


@login_required(login_url='/admin/login/')
def items_bar_finish_view(request,pk):
    if request.POST:
        item = Item.objects.filter(pk=pk,state="preparando").first()
        item.state = "finalizado"
        item.end_time = datetime.now()
        item.save()
    return render(request,'bar_and_kitchen/items/items_bar.html',context=all_charge_bar_items())
