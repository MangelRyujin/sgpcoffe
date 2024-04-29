from django.core.exceptions import ValidationError
import re


def validate_digits(value):
    if not value.isdigit():
        raise ValidationError("Este campo solo acepta dígitos.")
    
def validate_alpha(value):
    if not value.isalpha():
        raise ValidationError("Este campo solo acepta letras.")

def validate_alnum(value):
    if not value.isalnum():
        raise ValidationError("Este campo solo acepta letras y dígitos.")


def validate_letters_and_spaces(value):
    if not re.match(r'^[A-Za-z\sáéíóúÁÉÍÓÚ]*$', value):
        raise ValidationError(
            f'{value} contiene caracteres no permitidos. Solo se permiten letras y espacios en blanco.'
        )
        
def validate_letters_numbers_and_spaces(value):
    if not re.match(r'^[A-Za-z0-9\sáéíóúÁÉÍÓÚ]*$', value):
        raise ValidationError(
            f'Contiene caracteres no permitidos. Solo se permiten letras, números y espacios en blanco.'
        )