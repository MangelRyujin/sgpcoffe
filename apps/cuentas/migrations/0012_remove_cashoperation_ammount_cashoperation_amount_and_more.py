# Generated by Django 4.2 on 2024-05-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0011_alter_order_paid_method_cashoperation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashoperation',
            name='ammount',
        ),
        migrations.AddField(
            model_name='cashoperation',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Monto'),
        ),
        migrations.AlterField(
            model_name='cashoperation',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Dia de registro'),
        ),
        migrations.AlterField(
            model_name='cashoperation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='cashoperation',
            name='operation_type',
            field=models.CharField(choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto')], default='ingreso', max_length=13, verbose_name='Tipo de movimiento'),
        ),
        migrations.AlterField(
            model_name='cashoperation',
            name='payment_type',
            field=models.CharField(choices=[('transferencia', 'transferencia'), ('efectivo', 'efectivo')], default='efectivo', max_length=13, verbose_name='Método de pago'),
        ),
    ]