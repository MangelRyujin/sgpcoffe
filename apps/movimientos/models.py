from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.productos.models import PrincipalStock, Stock
User = get_user_model()
# Create your models here.


# Create model StockMovements.
class StockMovements(models.Model):
    TYPE_CHOICES  = (
        ('salida', 'salida'),
        ('entrada', 'entrada'),
        
    )
    MOTIVE_TYPE_CHOICES  = ( 
        ('reabastecer', 'reabastecer'),   #reabastecimiento
        ('pérdida', 'pérdida'),                #perdida
        ('cancelado', 'cancelado'),   #cancelado
        ('error', 'error'),                #error
        ('otro', 'otro'),                #otro
    )
    type = models.CharField('tipo',max_length=7, choices=TYPE_CHOICES, default='entrada') 
    created_date = models.DateField('fecha de creación',auto_now_add=True,null=True)
    created_time = models.TimeField('hora de creación',auto_now_add=True,null=True)
    motive = models.CharField('motivo',max_length=11, choices=MOTIVE_TYPE_CHOICES, default='reabastecer') 
    message = models.TextField('detalle',null=True,blank=True)
    cant = models.DecimalField('cantidad', max_digits=10, default=0, decimal_places=2, blank= False, null= False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('usuario'))
    stock=models.ForeignKey(Stock,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('almacenamiento stock'))

    class Meta:
        """Meta definition for StockMovements."""

        verbose_name = 'Movimiento en almacen'
        verbose_name_plural = 'Movimientos en stock'


    def __str__(self):
        return f"Movimiento realizado por el usario {self.user},dia {self.created_date} a las {self.created_time}"
    
    def clean(self):
        if self.type == 'salida':
            if self.stock.stock - self.cant < 0:
                raise ValidationError("La operación resultaría en un stock negativo.")


    def save(self, *args, **kwargs):
        if self.type == 'entrada':
            self.stock.update_stock(self.cant)
        elif self.type == 'salida':
            self.clean()
            self.stock.update_stock(-self.cant) 
        super().save(*args, **kwargs)
      
        
    def delete(self, *args, **kwargs):
        cant_before_deletion = self.cant
        if self.type == 'entrada':
            self.stock.update_stock(-cant_before_deletion)
        elif self.type == 'salida':
            self.stock.update_stock(cant_before_deletion)
        super().delete(*args, **kwargs)
        
# Create model PrincipalStockMovements.
class PrincipalStockMovements(models.Model):
    TYPE_CHOICES  = (
        ('salida', 'salida'),
        ('entrada', 'entrada'),
        
    )
    MOTIVE_TYPE_CHOICES  = ( 
        ('reabastecer', 'reabastecer'),   #reabastecimiento
        ('pérdida', 'pérdida'),                #perdida
        ('cancelado', 'cancelado'),   #cancelado
        ('error', 'error'),                #error
        ('otro', 'otro'),                #otro
    )
    type = models.CharField('tipo',max_length=7, choices=TYPE_CHOICES, default='entrada') 
    created_date = models.DateField('fecha de creación',auto_now_add=True,null=True)
    created_time = models.TimeField('hora de creación',auto_now_add=True,null=True)
    motive = models.CharField('motivo',max_length=11, choices=MOTIVE_TYPE_CHOICES, default='reabastecer') 
    message = models.TextField('detalle',null=True,blank=True)
    cant = models.DecimalField('cantidad', max_digits=10, default=0, decimal_places=2, blank= False, null= False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('usuario'))
    stock=models.ForeignKey(PrincipalStock,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('almacenamiento principal'))

    class Meta:
        """Meta definition for PrincipalStockMovements."""

        verbose_name = 'Movimiento en almacen principal'
        verbose_name_plural = 'Movimientos en almacen principal'


    def __str__(self):
        return f"Movimiento realizado por el usario {self.user},dia {self.created_date} a las {self.created_time}"
    
    def clean(self):
        if self.type == 'salida':
            if self.stock.stock - self.cant < 0:
                raise ValidationError("La operación resultaría en un stock negativo.")


    def save(self, *args, **kwargs):
        if self.type == 'entrada':
            self.stock.update_stock(self.cant)
        elif self.type == 'salida':
            self.clean()
            self.stock.update_stock(-self.cant) 
        super().save(*args, **kwargs)
      
        
    def delete(self, *args, **kwargs):
        cant_before_deletion = self.cant
        if self.type == 'entrada':
            self.stock.update_stock(-cant_before_deletion)
        elif self.type == 'salida':
            self.stock.update_stock(cant_before_deletion)
        super().delete(*args, **kwargs)