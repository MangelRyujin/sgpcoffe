from django.db import models
from solo.models import SingletonModel
from django.core.validators import MinValueValidator

class Coin(SingletonModel):
    rate = models.DecimalField('Valor de un dólar en CUP:', validators=[MinValueValidator(0.1)],max_digits=10, default=0, decimal_places=2, blank= True, null= True)
    active = models.BooleanField('Activo', default=False)

    def __str__(self):
        return 'Tasa de cambio'
    
    class Meta:
        verbose_name = "Tasa de cambio"
    