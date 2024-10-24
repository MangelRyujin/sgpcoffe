from django.contrib import admin

from apps.productos.models import AFT, Add, Category, Ingredient, Product, ProductAddRelation, ProductIngredientRelation, Stock, StockCategory, UtilProduct

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
    extra = 0
    
# Admin relations
class AddRelationsInline(admin.TabularInline):    
    model = ProductAddRelation    
    raw_id_fields = ('add',)
    extra = 0
    


# Admin Product 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','active','place','price']
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
    list_display = ['name','stock','disponible']
    search_fields = ['name','stock__name',]
    readonly_fields = ('disponible',)
    list_per_page = 100
    
# Admin UtilsProducts 
@admin.register(UtilProduct)
class UtilProductAdmin(admin.ModelAdmin):
    list_display = ['name','stock','disponible']
    search_fields = ['name','stock__name',]
    readonly_fields = ('disponible',)
    list_per_page = 100
    
    
# Admin AFT 
@admin.register(AFT)
class AFTAdmin(admin.ModelAdmin):
    list_display = ['name','price','cant']
    search_fields = ['name']
    list_per_page = 100

# Admin Stock 
@admin.register(StockCategory)
class StockCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 100

# Admin Stock 
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['name','stock','measure_unit','unit_price','storage_threshold','stock_category']
    search_fields = ['name','measure_unit','stock_category__name']
    list_filter = (
        'measure_unit',
        'stock_category'
    )
    readonly_fields = ('stock',)
    list_per_page = 100