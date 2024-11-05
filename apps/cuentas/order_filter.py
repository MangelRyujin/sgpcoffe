import django_filters
from django.contrib.auth.models import User
from apps.cuentas.models import Order
from apps.mesas.models import Table
from django.db.models import Q

class OrderFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    paid_method = django_filters.ChoiceFilter(choices=Order.PAID_METHODS_CHOICES)
    table = django_filters.ModelChoiceFilter(queryset=Table.objects.all())
    shift__in_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Order
        fields = ['user', 'paid_method','table','shift__in_date']
        
    