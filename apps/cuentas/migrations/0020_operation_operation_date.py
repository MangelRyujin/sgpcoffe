# Generated by Django 4.2 on 2024-09-08 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0019_operation'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='operation_date',
            field=models.DateField(null=True, verbose_name='Fecha de operación'),
        ),
    ]
