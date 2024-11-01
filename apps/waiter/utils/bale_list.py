
def bale_list(order):
    items = {}
    for item in order.item_set.filter(state="entregado"):
        if item.product.pk in items:
            items[item.product.pk]['cant']+= item.cant
            items[item.product.pk]['price']+=  item.estimate_price
        else:
            items[item.product.pk]={
                "product":item.product.name,
                "cant": item.cant,
                "price" : item.estimate_price
            }
    
    return items


