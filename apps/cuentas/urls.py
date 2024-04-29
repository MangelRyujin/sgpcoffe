from django.urls import path
from apps.cuentas.views import order_view



urlpatterns = [
    path('cuentas/',order_view,name='listar_cuentas'),
]