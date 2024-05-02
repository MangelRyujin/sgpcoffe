from django.core.exceptions import ValidationError
import re

from apps.cuentas.models import AddItem


def validate_product_discount_ingredient(item):
    error = ''
    for ingredient in item.product.ingredient_relations.all():
        discount = ingredient.ingredient.stock.stock - (ingredient.measure_unit_qty * item.cant)
        if discount < 0:
            error=f"No puede realizar el plato ya que hay un faltante de {discount} del ingrediente {ingredient.ingredient}"
            break
    return error
        