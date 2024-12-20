from django.contrib import admin
from django.contrib.admin import site
from django.contrib.admin import DateFieldListFilter

from apps.cuentas.models import *
# Register your models here.

# Admin add items
class AddItemInline(admin.TabularInline):    
    model = AddItem    
    raw_id_fields = ('add',)
    list_display = ('add',)
    extra = 0
    
# Admin add items
class IngredientItemInline(admin.TabularInline):    
    model = IngredientItem    
    raw_id_fields = ('ingredient',)
    list_display = ('ingredient',)
    extra = 0


admin.site.register(OperationType)

# # # Admin add items
class ItemInline(admin.TabularInline):    
    model = Item    
    raw_id_fields = ('product','order',)
    list_display = ('product','order',)
    # inlines = [AddItemInline]
    extra = 0
    

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['id','active','in_date','in_time','out_date','out_time', 'efectivo', 'transferencia', 'balance','revenue']
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
    list_display = ['id','table','user','is_paid','paid_method','shift','total_paid','created_date','created_time']
    search_fields = ['user__name','table','is_paid','paid_method','created_date']
    list_filter = (
        'user__username',
        'table__name',
        'is_paid',
        'paid_method',
        'created_date',
    )
    list_per_page = 100
    inlines = [ItemInline,]
 
@admin.register(CashOperation)
class CashOperationAdmin(admin.ModelAdmin):
    list_display = ('operation_type', 'shift', 'payment_type','type', 'amount', 'description', 'user' , 'created_date')
    list_select_related = ["shift", "user"]
    search_fields = ('operation_type', 'user__username', 'payment_type','type', 'description', 'created_date')
    list_filter = (
        'operation_type',
        'shift',
        'payment_type',
        'description',
        'type',
        'user',
        ('created_date', DateFieldListFilter),
    )
        
    list_per_page = 100
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    


# # Admin Items 
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['state','cant','total_price','product','order','created_time','end_time']
    search_fields = ['product__name','state']
    list_filter = (
        'state',
    )
    inlines = [AddItemInline,IngredientItemInline
               ]
 
 
# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ('id','order' ,'product', 'state', 'type', 'cant', 'total_price' , 'estimate_price','cost_price','revenue')
#     search_fields = ('product_name', 'type', 'state', 'description', 'created_date')
#     list_filter = (
#         'order',
#         'product',
#         'state',
#         'type',
#     )   
# admin.site.register(Item)
# admin.site.register(AddItem)
# admin.site.register(UtilsItem)
# admin.site.register(ItemMotiveCancelMessage)

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id' ,'operation_type', 'payment_type','type', 'amount', 'user' , 'created_date','operation_date')
    list_select_related = [ "user"]
    search_fields = ('operation_type', 'user__username', 'payment_type', 'description','operation_date','type')
    list_filter = (
        'operation_type',
        'payment_type',
        'description',
        'type',
        'user',
        # ('created_date', DateFieldListFilter),
        # ('operation_date', DateFieldListFilter),
    )
        
    list_per_page = 100