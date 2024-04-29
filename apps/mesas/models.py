from django.db import models

# Create your models here.


# Table  model
class Table(models.Model):
    """Model definition for Table."""
    
    PRODUCTION_PLACE_CHOICES = (
        ('ocupada', 'ocupada'),
        ('libre', 'libre'),
    )
    delivered = models.BooleanField("entrega rápida",default=False)
    state = models.CharField("estado",max_length=7, choices=PRODUCTION_PLACE_CHOICES, default='libre') 
    name = models.CharField('nombre', max_length=255, blank=False , null=False, unique=True)
    active = models.BooleanField("activo",default=True)

    # Define fields here

    class Meta:
        """Meta definition for Table."""

        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'

    def __str__(self):
        """Unicode representation of Table."""
        return f'{self.name}'
