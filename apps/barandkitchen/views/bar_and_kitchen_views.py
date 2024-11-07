from django.shortcuts import render
from apps.barandkitchen.utils.items import charge_items
from apps.cuentas.models import AddItem, Item, UtilsItem
from django.contrib.auth.decorators import login_required

from apps.productos.models import ProductAddRelation
from utils.product_validate.validate_ingredients_and_add_cant import validate_product_discount_ingredient 


@login_required(login_url='/admin/login/')
def bar_and_kitchen_elaboration_items(request):
    return render(request,'bar_and_kitchen/items_bar_and_kitchen.html',context=charge_items())

@login_required(login_url='/admin/login/')
def bar_and_kitchen_ordenado(request):
    return render(request,'bar_and_kitchen/items/items.html',context=charge_items())

@login_required(login_url='/admin/login/')
def items_proccess_view(request,pk):
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
    context=charge_items()
    context['error']=error
    return render(request,'bar_and_kitchen/items/items.html',context)


@login_required(login_url='/admin/login/')
def items_finish_view(request,pk):
    if request.POST:
        item = Item.objects.filter(pk=pk,state="preparando").first()
        item.state = "finalizado"
        item.save()
    return render(request,'bar_and_kitchen/items/items.html',context=charge_items())
