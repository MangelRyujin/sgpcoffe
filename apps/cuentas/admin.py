from django.contrib import admin
from django.contrib.admin import site
from apps.cuentas.models import Order,Item,AddItem,Shift, UtilsItem
# Register your models here.

# # Admin add items
# class AddItemInline(admin.TabularInline):    
#     model = AddItem    
#     raw_id_fields = ('add',)
#     list_display = ('add',)
#     extra = 0


# # # Admin add items
# class ItemInline(admin.TabularInline):    
#     model = Item    
#     raw_id_fields = ('product','order',)
#     list_display = ('product','order',)
#     inlines = [AddItemInline]
#     extra = 0
    

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['id','active','in_date','in_time','out_date','out_time']
    search_fields = ['in_date']
    list_per_page = 100
    
    def has_add_permission(self, request):
        if request.user.is_authenticated:
            active_shift = Shift.objects.filter(active=True).exists()
            if active_shift:
                return False
        return super().has_add_permission(request)
    
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
    # inlines = [ItemInline,]
 

    


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
admin.site.register(UtilsItem)

