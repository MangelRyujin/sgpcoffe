# Generated by Django 4.2 on 2024-04-24 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimientos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockmovements',
            name='cant',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='monto'),
        ),
    ]
