# Generated by Django 4.2 on 2024-11-01 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0021_item_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cost price'),
        ),
    ]