# Generated by Django 4.2 on 2024-04-29 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0009_remove_add_stock_remove_ingredient_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='expiration_date',
            field=models.DateField(blank=True, null=True, verbose_name='Próximo a vencer'),
        ),
    ]
