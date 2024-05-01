from django.shortcuts import render
from apps.cuentas.models import AddItem, Item, Order
from django.contrib.auth.decorators import login_required 


@login_required(login_url='/admin/login/')
def order_detail_view(request,pk):
    order = Order.objects.filter(pk=pk).first()
    items_delivered = []
    items_cancel = []
    for item in Item.objects.filter(order=order,state="entregado"):
       items_delivered.append({
           'delivered':item,
           'add': AddItem.objects.filter(
                            item = item
                        )
       })
    for item in Item.objects.filter(order=order,state="cancelado"):
       items_cancel.append({
           'cancel':item,
           'add': AddItem.objects.filter(
                            item = item
                        )
       })
    context ={"order":order,"items_delivered":items_delivered,"items_cancel":items_cancel}
    return render(request,'order_detail.html',context)