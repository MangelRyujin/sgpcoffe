from django.urls import path
from apps.cuentas.views.charts.chart_views import statistics_view
from apps.cuentas.views.charts.charts_data_views import get_filter_options,get_sales_chart,payment_success_chart,spend_per_customer_chart,payment_method_chart
from apps.cuentas.views.detail_order_views import order_detail_view
from apps.cuentas.views.list_order_views import order_view



urlpatterns = [
    path('cuentas/',order_view,name='orders_list'),
    path('cuenta/<int:pk>',order_detail_view,name='order_detail'),
    path('estadisticas/',statistics_view,name='statistics_orders'),
    path("chart/filter-options/", get_filter_options, name="chart-filter-options"),
    path("chart/sales/<int:year>/", get_sales_chart, name="chart-sales"),
    path("chart/payment-success/<int:year>/", payment_success_chart, name="chart-payment-success"),
    path("chart/spend-per-customer/<int:year>/", spend_per_customer_chart, name="chart-spend-per-customer"),
    path("chart/payment-method/<int:year>/", payment_method_chart, name="chart-payment-method"),
]