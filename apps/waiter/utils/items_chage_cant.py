

from apps.cuentas.models import AddItem
from apps.productos.models import ProductAddRelation


def increase_change_cant(item,cant_edit):
    message=''
    error=''
    if item.product.cant_discount_ingredients(cant_edit):
        item.product.discount_ingredients(cant_edit)
        for add in AddItem.objects.filter(item=item):
            product_add = ProductAddRelation.objects.get(add=add.add.id,product=item.product.id)
            product_add.discount_add(cant_edit,add.cant)
        message=f"Cantidad aumentada en {cant_edit}"
    else:
        print('negativo')
        error=f"Al parecer no contienes los suficientes elementos para aumentar"
    return message,error

def decrement_change_cant(item,cant_edit):
    item.product.revert_ingredients(cant_edit)
    for add in AddItem.objects.filter(item=item):
            product_add = ProductAddRelation.objects.get(add=add.add.id,product=item.product.id)
            product_add.revert_add(cant_edit,add.cant)
    return f"Cantidad disminuida en {cant_edit}"
