# Generated by Django 4.2 on 2024-04-24 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_remove_product_measure_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name of product')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cost')),
                ('measure_unit', models.CharField(default='unidades', max_length=255, verbose_name='Measure unit')),
                ('categories', models.ManyToManyField(blank=True, to='productos.category')),
            ],
            options={
                'verbose_name': 'Agregado',
                'verbose_name_plural': 'Agregados',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name of product')),
                ('measure_unit', models.CharField(default='unidades', max_length=255, verbose_name='Measure unit')),
                ('categories', models.ManyToManyField(blank=True, to='productos.category')),
            ],
            options={
                'verbose_name': 'Ingrediente',
                'verbose_name_plural': 'Ingredientes',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Stock')),
                ('measure_unit', models.CharField(default='unidades', max_length=255, verbose_name='Measure unit')),
            ],
            options={
                'verbose_name': 'Almacenamiento',
                'verbose_name_plural': 'Almacenamientos',
            },
        ),
        migrations.CreateModel(
            name='ProductIngredientRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measure_unit_qty', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cost')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_relations', to='productos.ingredient')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_relations', to='productos.product')),
            ],
            options={
                'unique_together': {('product', 'ingredient')},
            },
        ),
        migrations.CreateModel(
            name='ProductAddRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measure_unit_qty', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cost')),
                ('add', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='add_relations', to='productos.add')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='add_relations', to='productos.product')),
            ],
            options={
                'unique_together': {('product', 'add')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='added',
            field=models.ManyToManyField(blank=True, through='productos.ProductAddRelation', to='productos.add'),
        ),
        migrations.AddField(
            model_name='product',
            name='ingredients',
            field=models.ManyToManyField(blank=True, through='productos.ProductIngredientRelation', to='productos.ingredient'),
        ),
    ]
