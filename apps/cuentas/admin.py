from django.contrib import admin

from apps.cuentas.models import Order,Item,AddItem,Shift
# Register your models here.

# # Admin add items
# class AddItemInline(admin.TabularInline):    
#     model = AddItem    
#     raw_id_fields = ('add','item')
#     list_display = ('add','item')


# # Admin add items
# class ItemInline(admin.TabularInline):    
#     model = Item    
#     raw_id_fields = ('product','order')
#     list_display = ('product','order')
#     inlines = [AddItemInline,
#                ]

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['id','in_date','in_time','out_date','out_time']
    search_fields = ['in_date']
    list_per_page = 100
    
# Admin Order 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['table','user','is_paid','paid_method','shift','total_paid','created_date','created_time']
    search_fields = ['user__name','table','is_paid','paid_method','created_date']
    list_filter = (
        'user__username',
        'table__name',
        'is_paid',
        'paid_method',
        'created_date',
    )
    list_per_page = 100
 

    


# # Admin Items 
# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ['state','cant','total_price','product','order']
#     search_fields = ['product__name','state']
#     list_filter = (
#         'state',
#     )
#     inlines = [AddItemInline,
#                ]
 
    
admin.site.register(Item)
admin.site.register(AddItem)

