# Generated by Django 4.2 on 2024-05-26 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cuentas', '0013_alter_cashoperation_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashoperation',
            name='shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movimientos', to='cuentas.shift', verbose_name='Turno'),
        ),
        migrations.AlterField(
            model_name='cashoperation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientos', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
