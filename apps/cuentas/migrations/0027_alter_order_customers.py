# Generated by Django 4.2 on 2024-11-22 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0026_order_customers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customers',
            field=models.PositiveIntegerField(default=2, verbose_name='Cantidad de clientes'),
        ),
    ]
