
from django.contrib import admin

from apps.mesas.models import Table

# Register your models here.

# Admin Category
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['name','state','active','delivered']
    search_fields = ['name']
    list_filter = (
        'state',
        'active',
        'delivered',
    )
    list_per_page = 20
