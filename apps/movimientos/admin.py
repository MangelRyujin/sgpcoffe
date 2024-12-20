from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from apps.movimientos.models import HistoryStockMovements, PrincipalStockMovements, StockMovements

# Register your models here.

@admin.register(StockMovements)
class StockMovementsAdmin(admin.ModelAdmin):
    list_display = ['type', 'motive','cant','user' ,'created_date','created_time','stock']
    search_fields = ['type', 'motive','user__username','created_date']
    list_filter = (
        ('created_date', DateFieldListFilter),
        'type',
        'motive',
        'user',
        'stock',
        
    )
    list_per_page = 100
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
@admin.register(PrincipalStockMovements)
class PrincipalStockMovementsAdmin(admin.ModelAdmin):
    list_display = ['type', 'motive','cant','user' ,'created_date','created_time','stock']
    search_fields = ['type', 'motive','user__username','created_date']
    list_filter = (
        ('created_date', DateFieldListFilter),
        'type',
        'motive',
        'user',
        'stock',
        
    )
    list_per_page = 100
    
    def has_change_permission(self, request, obj=None):
        return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    
@admin.register(HistoryStockMovements)
class HistoryStockMovementsAdmin(admin.ModelAdmin):
    list_display = ['movement','stock', 'movimiento','can_change','cantidad_actualizada_despues_del_movimiento_actual','unit_price']
    search_fields = ['movement__stock__name']
    list_per_page = 500
    readonly_fields = ('movimiento','cantidad_actualizada_despues_del_movimiento_actual','cantidad_actual')
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def has_delete_permission(self, request, obj=None):
        return False