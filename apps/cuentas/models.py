from django.db import models
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.mesas.models import Table
from apps.productos.models import Add, Product
User = get_user_model()

    
# Order model.
class Order(models.Model):
    PAID_CHOICES = (
        ('pagada', 'pagada'),
        ('no pagada', 'no pagada'),
    )
    PAID_METHODS_CHOICES = (
        ('transferencia', 'transferencia'),
        ('efectivo', 'cash'),
        ('ambos', 'ambos'),
    )
    is_paid = models.CharField('estado',max_length=9, choices=PAID_CHOICES, default='no pagada') 
    paid_method = models.CharField('mótodo de pago',max_length=13, choices=PAID_METHODS_CHOICES, default='efectivo') 
    total_paid = models.DecimalField('Precio total', max_digits=10, default=0, decimal_places=2, blank= True, null= True)
    created_date = models.DateField('dia de apertura',auto_now_add=True,null=True)
    created_time = models.TimeField('hora de apertura',auto_now_add=True,null=True)
    table = models.ForeignKey(Table,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('mesa')) 
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('usuario'))
    
    class Meta:   
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'

    def __str__(self) -> str:
        return f'Cuenta {self.pk} de la mesa {self.table}'

    
# Order item model.
class Item(models.Model):
    STATE_CHOICES = (
        ('ordenado', 'ordenado'),
        ('finalizado', 'finalizado'),
        ('entregado', 'entregado'),
        ('cancelado', 'cancelado'),
    )
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='ordenado') 
    cant = models.PositiveIntegerField("Cant",default=1,null=False,blank=False)
    total_price = models.DecimalField('Total price', max_digits=10, default=0, decimal_places=2, blank= True, null= True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('producto'))
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('cuenta'))
    
    class Meta:   
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self) -> str:
        return f'Pedido de {self.product}'
    
# Order add item model.
class AddItem(models.Model):
    cant = models.PositiveIntegerField("Cant",default=1,null=False,blank=False)
    add = models.ForeignKey(Add,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('agregado'))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True,verbose_name=_('pedido'))
    
    class Meta:   
        verbose_name = 'Agregado de pedido'
        verbose_name_plural = 'Agregados de pedidos'

    def __str__(self) -> str:
        return f'Agregado {self.add.name}'
