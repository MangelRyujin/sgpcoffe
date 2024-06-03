from django.urls import path
from apps.cuentas.views.charts.chart_views import statistics_view
from apps.cuentas.views.charts.charts_data_views import get_filter_options,get_sales_chart,payment_success_chart,spend_per_customer_chart
from apps.cuentas.views.charts.charts_month_data_views import get_day_sales_chart, get_month_filter_options, spend_month_per_customer_chart,payment_month_success_chart
from apps.cuentas.views.detail_order_views import order_detail_view
from apps.cuentas.views.list_order_views import order_view
from apps.cuentas.views.unpaid_order.detail_unpaid_order_views import form_item_create_view, product_sell_view, unpaid_order_detail_view
from apps.cuentas.views.unpaid_order.items_views import form_item_delete_view,form_create_add_item_view,form_create_util_item_view
from apps.cuentas.views.unpaid_order.list_unpaid_order_views import unpaid_order_view



urlpatterns = [
    path('cuentas/',order_view,name='orders_list'),
    path('cuenta/<int:pk>',order_detail_view,name='order_detail'),
    path('cuenta/<int:order>/item/<int:pk>',form_item_delete_view,name='delete_item_form'),
    path('cuenta/<int:order>/item/<int:pk>/cancel',form_item_delete_view,name='cancel_item_form'),
    path('cuenta/<int:order>/item/<int:pk>/add/create',form_create_add_item_view,name='create_add_item_form'),
    path('cuenta/<int:order>/item/<int:pk>/util/create',form_create_util_item_view,name='create_util_item_form'),
    path('gestionar/cuentas/',unpaid_order_view,name='unpaid_orders_list'),
    path('gestionar/cuenta/<int:pk>',unpaid_order_detail_view,name='unpaid_order_detail'),
    path('gestionar/cuenta/<int:order>/product/<int:pk>',form_item_create_view,name='create_item_form'),
    path('gestionar/cuentas/<int:order>/products/',product_sell_view,name='product_sell_list'),
    path('estadisticas/',statistics_view,name='statistics_orders'),
    path("chart/filter-options/", get_filter_options, name="chart-filter-options"),
    path("chart/sales/<int:year>/", get_sales_chart, name="chart-sales"),
    path("chart/payment-success/<int:year>/", payment_success_chart, name="chart-payment-success"),
    path("chart/spend-per-customer/<int:year>/", spend_per_customer_chart, name="chart-spend-per-customer"),
    path("chart/month/filter-options/", get_month_filter_options, name="chart-month-filter-options"),
    path("chart/day/sales/<int:month>/<int:monthYear>/", get_day_sales_chart, name="chart-day-sales"),
    path("chart/month/spend-per-customer/<int:month>/<int:monthYear>/", spend_month_per_customer_chart, name="chart-month-spend-per-customer"),
    path("chart/month/payment-success/<int:month>/<int:monthYear>/", payment_month_success_chart, name="chart-month-payment-success"),
    
]