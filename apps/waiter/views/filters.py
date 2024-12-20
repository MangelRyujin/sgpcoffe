import django_filters

from apps.productos.models import Product

class ProductFilter(django_filters.FilterSet):
    name=  django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name']