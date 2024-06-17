from django.core.exceptions import ValidationError
import re

from apps.cuentas.models import AddItem, UtilsItem


def validate_product_discount_ingredient(item):
    error = ''
    for ingredient in item.product.ingredient_relations.all():
        discount = ingredient.ingredient.stock.stock - (ingredient.measure_unit_qty * item.cant)
        if discount < 0:
            error=f"No puede realizar el plato ya que hay un faltante de {discount} {ingredient.ingredient.stock.measure_unit} del ingrediente {ingredient.ingredient}"
            break
    for add in AddItem.objects.filter(item=item):
        product_add = item.product.add_relations.get(add = add.add.id )
        if add.add.stock.stock - ((product_add.measure_unit_qty * add.cant)*item.cant) < 0:
            error=f"No puede realizar el plato ya que hay un faltante de {add.add.stock.stock - add.cant} {add.add.stock.measure_unit} del agregado {add.add.name}"
            break
    for util in UtilsItem.objects.filter(item=item):
        if util.util.stock.stock - util.cant < 0:
            error=f"No puede realizar el plato ya que hay un faltante de {util.util.stock.stock - util.cant} {util.util.stock.measure_unit} del util {util.util.name}"
            break
    return error
        