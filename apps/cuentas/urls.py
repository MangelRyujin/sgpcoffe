from django.urls import path
from apps.cuentas.views.detail_order_views import order_detail_view
from apps.cuentas.views.list_order_views import order_view



urlpatterns = [
    path('cuentas/',order_view,name='orders_list'),
    path('cuenta/<int:pk>',order_detail_view,name='order_detail'),
]