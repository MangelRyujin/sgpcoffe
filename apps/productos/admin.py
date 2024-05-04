from django.contrib import admin

from apps.productos.models import Add, Category, Ingredient, Product, ProductAddRelation, ProductIngredientRelation, Stock

# Register your models here.

# Admin Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','type']
    search_fields = ['name']
    list_filter = (
        'type',
    )
    list_per_page = 100


# Admin relations
class IngredientsRelationsInline(admin.TabularInline):    
    model = ProductIngredientRelation    
    raw_id_fields = ('ingredient',)
    list_display = ('ingredient')
    
# Admin relations
class AddRelationsInline(admin.TabularInline):    
    model = ProductAddRelation    
    raw_id_fields = ('product','add',)
    list_display = ('add')
    


# Admin Product 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','active','place','price','price']
    search_fields = ['name','categories__name',]
    list_filter = (
        'place',
        'active',
    )
    inlines = [IngredientsRelationsInline,
               AddRelationsInline,
               ]
    list_per_page = 100
 
    

# Admin Ingredient 
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name','stock','disponible']
    search_fields = ['name','stock__name',]
    readonly_fields = ('disponible',)
    list_per_page = 100
    
    
# Admin Add 
@admin.register(Add)
class AddAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','disponible']
    search_fields = ['name','stock__name',]
    readonly_fields = ('disponible',)
    list_per_page = 100

# Admin Stock 
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['name','stock','measure_unit']
    search_fields = ['name','measure_unit',]
    list_filter = (
        'measure_unit',
    )
    readonly_fields = ('stock',)
    list_per_page = 100