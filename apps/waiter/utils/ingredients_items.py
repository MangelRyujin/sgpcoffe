from apps.cuentas.models import IngredientItem


def create_ingredients_item(item):
        for ingredient in item.product.ingredient_relations.all():
            cant = ingredient.measure_unit_qty * item.cant
            IngredientItem.objects.create(
                    item=item,
                    ingredient = ingredient.ingredient,
                    cant= cant,
                    cost= cant * ingredient.ingredient.stock.unit_price
                )
            
def remove_ingredients_item(item):
    item_ingredients = item.ingredientitem_set.all()
    item_ingredients.delete()
    create_ingredients_item(item)
    