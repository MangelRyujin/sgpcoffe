# Generated by Django 4.2 on 2024-04-24 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_alter_productaddrelation_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='active',
        ),
        migrations.AlterField(
            model_name='add',
            name='measure_unit',
            field=models.CharField(default='unidades', max_length=255, verbose_name='unidad de medida'),
        ),
        migrations.AlterField(
            model_name='add',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='add',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='precio'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('vendible', 'vendible'), ('no vendible', 'no vendible')], default='vendible', max_length=13, verbose_name='tipo'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measure_unit',
            field=models.CharField(default='unidades', max_length=255, verbose_name='unidad de medida'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True, verbose_name='activo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.FloatField(default=0.0, verbose_name='descuento en %'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_image/', verbose_name='imagen'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='product',
            name='place',
            field=models.CharField(choices=[('cocina', 'cocina'), ('bar', 'bar')], default='cocina', max_length=7, verbose_name='lugar de elaboración'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='precio'),
        ),
        migrations.AlterField(
            model_name='productaddrelation',
            name='measure_unit_qty',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='cantidad'),
        ),
        migrations.AlterField(
            model_name='productaddrelation',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='precio'),
        ),
        migrations.AlterField(
            model_name='productingredientrelation',
            name='measure_unit_qty',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='cantidad'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='measure_unit',
            field=models.CharField(default='unidades', max_length=255, verbose_name='unidad de medida'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='almacenamiento en stock'),
        ),
    ]