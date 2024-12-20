# Generated by Django 4.2 on 2024-10-27 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0017_principalstock'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movimientos', '0004_alter_stockmovements_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockmovements',
            name='cant',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='cantidad'),
        ),
        migrations.CreateModel(
            name='PrincipalStockMovements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('salida', 'salida'), ('entrada', 'entrada')], default='entrada', max_length=7, verbose_name='tipo')),
                ('created_date', models.DateField(auto_now_add=True, null=True, verbose_name='fecha de creación')),
                ('created_time', models.TimeField(auto_now_add=True, null=True, verbose_name='hora de creación')),
                ('motive', models.CharField(choices=[('reabastecer', 'reabastecer'), ('pérdida', 'pérdida'), ('cancelado', 'cancelado'), ('error', 'error'), ('otro', 'otro')], default='reabastecer', max_length=11, verbose_name='motivo')),
                ('message', models.TextField(blank=True, null=True, verbose_name='detalle')),
                ('cant', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='cantidad')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.principalstock', verbose_name='almacenamiento principal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuario')),
            ],
            options={
                'verbose_name': 'Movimiento en almacen principal',
                'verbose_name_plural': 'Movimientos en almacen principal',
            },
        ),
    ]
