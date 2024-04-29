from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from apps.movimientos.models import StockMovements

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
    
    def has_change_permission(self, request, obj=None):
        return False