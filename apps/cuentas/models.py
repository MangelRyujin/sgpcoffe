from django.db import models
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.coins.models import Coin
from apps.mesas.models import Table
from apps.productos.models import Add, Product, ProductAddRelation, UtilProduct
from django.contrib import admin
from django.db.models import Sum
from decimal import Decimal 



User = get_user_model()

    
class Operation(models.Model):
    MOVEMENT_TYPES_CHOICES = (
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    )
    PAYMENT_METHODS_CHOICES = (
        ('transferencia', 'Transferencia'),
        ('efectivo', 'Efectivo'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('Usuario'), related_name='user_operation')
    operation_type = models.CharField('Tipo de movimiento',max_length=13, choices=MOVEMENT_TYPES_CHOICES, default='ingreso')
    payment_type = models.CharField('Método de pago',max_length=13, choices=PAYMENT_METHODS_CHOICES, default='efectivo')
    amount = models.DecimalField('Monto', max_digits=10, default=0, decimal_places=2, blank= True, null= True)
    description = models.TextField('Descripción',null=True,blank=True)
    created_date = models.DateField('Día de registro',auto_now_add=True,null=True)
    operation_date = models.DateField('Fecha de operación',auto_now_add=False,null=True)
    
    def __str__(self) -> str:
        return f'Movimiento: {self.operation_type}, en {self.payment_type}, en un monto de {self.amount}'
    
    class Meta:
        verbose_name = 'Operacione'
        verbose_name_plural = 'Operaciones'
    

# Shift model.
class Shift(models.Model):
    in_date = models.DateField('Fecha de inicio de turno')
    in_time = models.TimeField('Hora de inicio de turno')
    out_date = models.DateField('Fecha de fin de turno')
    out_time = models.TimeField('Hora de fin de turno')
    active = models.BooleanField("activo",default=True)
    revenue = models.DecimalField('Ganancia', max_digits=10, default=0, decimal_places=2,editable=False, blank= True, null= True)
    
    # Balance de efectivo del turno por movimientos de caja y ventas
    @property
    @admin.display(
        description="Saldo en efectivo",
        boolean=True,
    )
    def efectivo(self):
        total_ventas_efectivo = self.orders.all().aggregate(Sum('cash'))['cash__sum'] or Decimal(0.0)
        total_efectivo_ingreso = self.movimientos.filter(payment_type='efectivo',operation_type='ingreso').aggregate(Sum('amount'))['amount__sum'] or Decimal(0.0)
        total_efectivo_gasto = self.movimientos.filter(payment_type='efectivo',operation_type='gasto').aggregate(Sum('amount'))['amount__sum'] or Decimal(0.0)
        return Decimal(total_ventas_efectivo + total_efectivo_ingreso - total_efectivo_gasto).quantize(Decimal('.01'))
    
    # Balance de transferencias del turno por movimientos de caja y ventas
    @property
    @admin.display(
        description="Saldo en transferencias",
        boolean=True,
    )
    def transferencia(self):
        total_ventas_transferencia = self.orders.all().aggregate(Sum('transfer'))['transfer__sum'] or Decimal(0.0)
        total_transferencia_ingreso = self.movimientos.filter(payment_type='transferencia',operation_type='ingreso').aggregate(Sum('amount'))['amount__sum'] or 0
        total_transferencia_gasto = self.movimientos.filter(payment_type='transferencia',operation_type='gasto').aggregate(Sum('amount'))['amount__sum'] or 0
        return Decimal(total_ventas_transferencia + total_transferencia_ingreso - total_transferencia_gasto).quantize(Decimal('.01'))
    
    # Balance de la caja en el turno por movimientos de caja y ventas
    @property
    @admin.display(
        description="Recaudación total en el turno",
        boolean=True,
    )
    def balance(self):
        total_ventas_efectivo = self.orders.all().aggregate(Sum('cash'))['cash__sum'] or Decimal(0.0)
        total_ventas_transferencia = self.orders.all().aggregate(Sum('transfer'))['transfer__sum'] or Decimal(0.0)
        total_ingresos_movimientos = self.movimientos.filter(operation_type='ingreso').aggregate(Sum('amount'))['amount__sum'] or 0
        total_gastos_movimientos = self.movimientos.filter(operation_type='gasto').aggregate(Sum('amount'))['amount__sum'] or 0
        total = total_ventas_efectivo + total_ventas_transferencia + total_ingresos_movimientos - total_gastos_movimientos
        return Decimal(total).quantize(Decimal('.01'))
    
    
    @property
    def shift_transfer_operations(self):
        total_income_operations = self.movimientos.filter(operation_type='ingreso',payment_type="transferencia").aggregate(Sum('amount'))['amount__sum'] or 0
        total_spent_operations = self.movimientos.filter(operation_type='gasto',payment_type="transferencia").aggregate(Sum('amount'))['amount__sum'] or 0
        return total_income_operations - total_spent_operations
    
    @property
    def shift_cash_operations(self):
        total_income_operations = self.movimientos.filter(operation_type='ingreso',payment_type="efectivo").aggregate(Sum('amount'))['amount__sum'] or 0
        total_spent_operations = self.movimientos.filter(operation_type='gasto',payment_type="efectivo").aggregate(Sum('amount'))['amount__sum'] or 0
        return total_income_operations - total_spent_operations
    
    @property
    def shift_total_operations(self):
        return self.shift_transfer_operations + self.shift_cash_operations 
    
    class Meta:   
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'

    def __str__(self) -> str:
        return f'Turno {self.pk}'
    
    def add_revenue(self,revenue):
        self.revenue+= revenue
        self.save()


# Modelo de gastos/ingresos en el turno (movimiento de dinero)
'''
No edición en el admin
turno
usuario
tipo (ingreso o gasto)
descripcion null
monto (decimal)
metodo de pago (tranf o efectivo)
fecha y hora
'''
class CashOperation(models.Model):
    MOVEMENT_TYPES_CHOICES = (
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    )
    PAYMENT_METHODS_CHOICES = (
        ('transferencia', 'Transferencia'),
        ('efectivo', 'Efectivo'),
    )
    shift = models.ForeignKey(Shift,on_delete=models.CASCADE,null=True,blank=True,verbose_name=_('Turno'), related_name='movimientos') 
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('Usuario'), related_name='movimientos')
    operation_type = models.CharField('Tipo de movimiento',max_length=13, choices=MOVEMENT_TYPES_CHOICES, default='ingreso')
    payment_type = models.CharField('Método de pago',max_length=13, choices=PAYMENT_METHODS_CHOICES, default='efectivo')
    amount = models.DecimalField('Monto', max_digits=10, default=0, decimal_places=2, blank= True, null= True)
    description = models.TextField('Descripción',null=True,blank=True)
    created_date = models.DateField('Día de registro',auto_now_add=True,null=True)
    
    def __str__(self) -> str:
        return f'Turno {self.shift.pk}. Movimiento: {self.operation_type}, en {self.payment_type}, en un monto de {self.amount}'
    
    class Meta:
        verbose_name = 'Movimiento de caja'
        verbose_name_plural = 'Movimientos de caja'
    
    
    
# Order model.
class Order(models.Model):
    PAID_CHOICES = (
        ('pagada', 'pagada'),
        ('no pagada', 'no pagada'),
    )
    PAID_METHODS_CHOICES = (
        ('transferencia', 'transferencia'),
        ('efectivo', 'efectivo'),
        ('ambos', 'ambos'),
    )
    is_paid = models.CharField('estado',max_length=9, choices=PAID_CHOICES, default='no pagada') 
    paid_method = models.CharField('método de pago',max_length=13, choices=PAID_METHODS_CHOICES, default='efectivo') 
    transfer = models.DecimalField('Pagado por transferencia', max_digits=10, default=0, decimal_places=2, blank= True, null= True)
    cash = models.DecimalField('Pagado por efectivo', max_digits=10, default=0, decimal_places=2, blank= True, null= True)
    shift = models.ForeignKey(Shift,on_delete=models.CASCADE,null=True,blank=True,verbose_name=_('turno'), related_name='orders') 
    created_date = models.DateField('dia de apertura',auto_now_add=True,null=True)
    created_time = models.TimeField('hora de apertura',auto_now_add=True,null=True)
    table = models.ForeignKey(Table,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('mesa')) 
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('usuario'))
    
    class Meta:   
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'

    def __str__(self) -> str:
        return f'Cuenta {self.pk}'

    @property
    def order_delete(self):
        items=self.item_set.exclude(state="ordenado")
        if items.exists():
            return False
        return True
    
    @property
    def order_cant_paid(self):
        items=self.item_set.filter(state__in=['ordenado','preparando','finalizado']).first()
        if items:
            return False
        return True
    
    @property
    def contain_item_message(self):
        for item in self.item_set.all():
            if item.message:
                return True
        return False
    

    @property
    def total_paid(self):
        return self.transfer + self.cash
    
    @property
    def total_price(self):
        total = Decimal(0)
        for item in Item.objects.filter(order=self,state="entregado"):
            total+=item.total_price
        return total
    
    @property
    def rate(self):
        rate = Coin.objects.first()
        if rate:
            return round(self.total_price/rate.rate,2) if rate.active else 0.0
        return 0.0
            
    
    
# Order item model.
class Item(models.Model):
    STATE_CHOICES = (
        ('ordenado', 'ordenado'),
        ('preparando','preparando'),
        ('finalizado', 'finalizado'),
        ('entregado', 'entregado'),
        ('cancelado', 'cancelado'),
    )
    TYPE_CHOICES = (
        ('llevar', 'llevar'),
        ('local','local'),
    )
    is_active = models.BooleanField(default=False)
    message= models.TextField(blank=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='ordenado') 
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='local') 
    cant = models.PositiveIntegerField("Cant",default=1,null=False,blank=False)
    total_price = models.DecimalField('Total price', max_digits=10, default=0, decimal_places=2, blank= True, null= True)
    revenue_price = models.DecimalField('Revenue price', max_digits=10, default=0, decimal_places=2, blank= True, null= True)
    cost_price = models.DecimalField('Cost price', max_digits=10, default=0, decimal_places=2)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('producto'))
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('cuenta'))
    
    class Meta:   
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self) -> str:
        return f'Pedido de {self.product}'
    
    @property
    def total_cost(self):
        return self.total_price-self.revenue_price
    
    @property
    def estimate_price(self):
        product_price=self.product.discount_price * self.cant 
        total_add_cost = Decimal(0)
        total_util_cost = Decimal(0)
        for add_item in AddItem.objects.filter(item=self):
            product_add_relation = ProductAddRelation.objects.get(
                    product=self.product,
                    add=add_item.add
            )
            total_add_cost+=(product_add_relation.price*add_item.cant)*self.cant
        for util_item in UtilsItem.objects.filter(item=self):
            total_util_cost+=util_item.util.price*util_item.cant
        return product_price + total_add_cost + total_util_cost
    
    @property
    def inversion_cost(self):
        revenue = Decimal(0)
        for ingredient in self.product.ingredient_relations.all():
            revenue+=ingredient.ingredient.stock.unit_price*ingredient.measure_unit_qty
        for add in AddItem.objects.filter(item = self):
            add_item = add.add.add_relations.filter(add=add.add.id,product=self.product.id).first()
            revenue+= (add_item.add.stock.unit_price*add_item.measure_unit_qty)*add.cant
        for util in UtilsItem.objects.filter(item = self):
            revenue+= util.util.stock.unit_price*util.cant
        revenue= revenue*self.cant
        return round(revenue,2)
    
    
    @property
    def revenue(self):
        return self.estimate_price - self.inversion_cost
    
    
# Order add item model.
class AddItem(models.Model):
    cant = models.PositiveIntegerField("Cant",default=1,null=False,blank=False)
    add = models.ForeignKey(Add,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('agregado'))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True,verbose_name=_('pedido'))
    
    class Meta:   
        verbose_name = 'Agregado de pedido'
        verbose_name_plural = 'Agregados de pedidos'

    def __str__(self) -> str:
        return f'Item agregado {self.add.name}'


# Order UtilsItem model.
class UtilsItem(models.Model):
    cant = models.PositiveIntegerField("Cant",default=1,null=False,blank=False)
    util = models.ForeignKey(UtilProduct,on_delete=models.CASCADE,null=False,blank=False,verbose_name=_('útil'))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True,verbose_name=_('pedido'))
    
    class Meta:   
        verbose_name = 'Útil de pedido'
        verbose_name_plural = 'Útiles de pedidos'

    def __str__(self) -> str:
        return f'Útil {self.util.name}'
    
    def discount_util(self):
        self.util.stock.stock-=self.cant
        self.util.stock.save()
    
    
# ItemMotiveCancelMessage model.
class ItemMotiveCancelMessage(models.Model):
    motive = models.TextField("Motivo",default="",null=True,blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True,verbose_name=_('pedido'))
    
    class Meta:   
        verbose_name = 'Motivo'
        verbose_name_plural = 'Motivos'

    def __str__(self) -> str:
        return f'Motive by item {self.item}'
    

    