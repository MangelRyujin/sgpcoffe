from django.db import models
from utils.validates.validates import validate_letters_numbers_and_spaces
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.




# Stock  model
class Stock(models.Model):
    MEASURE_UNIT_CHOICES = (
        ('mililitros', 'mililitros'),
        ('gramos', 'gramos'),
        ('unidades', 'unidades'),
    )
    
    name=models.CharField('nombre',max_length=100,blank=False,null=False)
    stock=models.DecimalField('almacenamiento en stock', max_digits=10, default=0, decimal_places=2, blank= False, null= False)
    measure_unit = models.CharField("unidad de medida",max_length=13, choices=MEASURE_UNIT_CHOICES, default='unidades') 
    
    class Meta:
        verbose_name = "Almacenamiento"
        verbose_name_plural = "Almacenamientos"

    def __str__(self):
        return f'{self.name}'
    
    def update_stock(self, quantity):
        self.stock = self.stock + quantity
        self.save()


# Category model
class Category(models.Model):
    CATEGORY_TYPE_CHOICES = (
        ('vendible', 'vendible'),
        ('no vendible', 'no vendible'),
    )
    type = models.CharField("tipo",max_length=13, choices=CATEGORY_TYPE_CHOICES, default='vendible') 
    name = models.CharField('nombre', max_length=255, blank=False , null=False)
    
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name
    
    

    
# Ingredient  model
class Ingredient(models.Model):
    """Model definition for Ingredient."""
    name = models.CharField('nombre', max_length=255, blank=False , null=False)
    categories = models.ManyToManyField(Category,blank=True,verbose_name=_('categorias') )
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE,blank=False,verbose_name=_('almacenamiento stock') )
    
    
    # Define fields here

    class Meta:
        """Meta definition for Ingredient."""

        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'

    def __str__(self):
        """Unicode representation of Ingredient."""
        return f'{self.name}'

    @property
    def disponible(self):
        return f'{self.stock.stock} {self.stock.measure_unit}'

    
# Add  model
class Add(models.Model):
    """Model definition for Add."""
    name = models.CharField('nombre', max_length=255, blank=False , null=False)
    price = models.DecimalField('precio', max_digits=10, default=0, decimal_places=2, blank= False, null= False)
    categories = models.ManyToManyField(Category,blank=True,verbose_name=_('categorias') )
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE,blank=False,verbose_name=_('almacenamiento stock') )
    
    
    # Define fields here

    class Meta:
        """Meta definition for Add."""

        verbose_name = 'Agregado'
        verbose_name_plural = 'Agregados'

    def __str__(self):
        """Unicode representation of Add."""
        return f'{self.name}'

    @property
    def disponible(self):
        return f'{self.stock.stock} {self.stock.measure_unit}'



    
# Product  model
class Product(models.Model):
    """Model definition for Product."""
    
    PRODUCTION_PLACE_CHOICES = (
        ('cocina', 'cocina'),
        ('bar', 'bar'),
    )
    place = models.CharField("lugar de elaboración",max_length=7, choices=PRODUCTION_PLACE_CHOICES, default='cocina') 
    name = models.CharField('nombre', max_length=255, blank=False , null=False)
    price = models.DecimalField('precio', max_digits=10, default=0, decimal_places=2, blank= False, null= False)
    discount = models.FloatField('descuento en %',default=0.0)
    active = models.BooleanField("activo",default=True)
    image = models.ImageField('imagen', upload_to='product_image/', blank=True, null=True)
    categories = models.ManyToManyField(Category,blank=True ,verbose_name=_('categorias'))
    ingredients = models.ManyToManyField(Ingredient, through='ProductIngredientRelation',through_fields=('product','ingredient'), blank=True)
    added = models.ManyToManyField(Add, through='ProductAddRelation',through_fields=('product','add'), blank=True)
    
    
    # Define fields here

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        """Unicode representation of Product."""
        return f'{self.name}'



# Product add relation ManyToMany
class ProductIngredientRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredient_relations',verbose_name=_('producto'))
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_relations',verbose_name=_('ingrediente'))
    measure_unit_qty = models.DecimalField('cantidad', max_digits=10, default=0, decimal_places=2, blank= False, null= False)
    
    class Meta:
        unique_together = ('product', 'ingredient',)
        verbose_name = 'Relación de productos e ingredientes'
        verbose_name_plural = 'Relación de productos e ingredientes'
        
    def __str__(self):
        """Unicode representation of ProductIngredient."""
        return f'Ingrediente {self.ingredient.name} asignado al producto {self.product.name} con {self.measure_unit_qty}'
    



# Product add relation ManyToMany
class ProductAddRelation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='add_relations',verbose_name=_('producto'))
    add = models.ForeignKey(Add, on_delete=models.CASCADE, related_name='add_relations',verbose_name=_('agregado'))
    measure_unit_qty = models.DecimalField('cantidad', max_digits=10, default=0, decimal_places=2, blank= False, null= False)
    price = models.DecimalField('precio', max_digits=10, default=0, decimal_places=2, blank= False, null= False)
    
    class Meta:
        unique_together = ('product', 'add',)
        verbose_name = 'Relación de productos y agregados'
        verbose_name_plural = 'Relación de productos y agregados'
        
    def __str__(self):
        """Unicode representation of ProductAdd."""
        return f'Relación de {self.product.name} con  {self.add.name}'