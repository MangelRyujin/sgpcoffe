# Generated by Django 4.2 on 2024-12-20 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0018_alter_product_place'),
        ('cuentas', '0029_operationtype_cashoperation_type_operation_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cantidad')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Decimal')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='productos.ingredient', verbose_name='ingrediente')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cuentas.item', verbose_name='pedido')),
            ],
            options={
                'verbose_name': 'Ingrediente de pedido',
                'verbose_name_plural': 'Ingredientes de pedidos',
            },
        ),
    ]
