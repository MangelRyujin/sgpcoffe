
from django.urls import path
from apps.reportes.views.charts.product_charts_data_month_price_views import get_day_sales_price_chart,spend_month_per_customer_price_chart,payment_month_success_price_chart
from apps.reportes.views.charts.product_charts_data_month_views import get_day_sales_chart, get_filter_month_options,spend_month_per_customer_chart,payment_month_success_chart

from apps.reportes.views.charts.product_charts_data_views import product_statistics_view
from apps.reportes.views.charts.product_charts_data_anual_views import get_filter_options,get_product_sales_chart,spend_product_per_customer_chart,payment_product_success_chart
from apps.reportes.views.charts.product_charts_data_anual_price_views import get_product_sales_price_chart,spend_product_per_customer_price_chart,payment_product_success_price_chart

from apps.reportes.views.reports_views import reports_view
from apps.reportes.views.reports_warehouses_views import reports_warehouses_stock_movement_view, reports_warehouses_stock_principal_movement_view, reports_warehouses_view



urlpatterns = [
    path('',reports_view,name='reports_view'),
    path('estadisticas-de-productos/',product_statistics_view,name='product_statistics_orders'),
    path('estadisticas/anual/options/list/',get_filter_options,name='product_options_statistics'),
    path('estadisticas/month/options/list/',get_filter_month_options,name='product_options_month_statistics'),
    # cant anual
    path("estadisticas/anual/sales/<int:year>/<str:product>/<str:product2>/<str:product3>/", get_product_sales_chart, name="product-anual-sales"),
    path("estadisticas/anual/sales/spend-per-customer/<int:year>/<str:product>/<str:product2>/<str:product3>/", spend_product_per_customer_chart, name="product-anual-sales-spend-per-customer"),
    path("estadisticas/anual/sales/payment-success/<int:year>/<str:product>/<str:product2>/<str:product3>/", payment_product_success_chart, name="product-anual-payment-success"),
    # price anual
    path("estadisticas/anual/sales/price/<int:year>/<str:product>/<str:product2>/<str:product3>/", get_product_sales_price_chart, name="product-anual-sales-price"),
    path("estadisticas/anual/sales/price/spend-per-customer/<int:year>/<str:product>/<str:product2>/<str:product3>/", spend_product_per_customer_price_chart, name="product-anual-sales-price-spend-per-customer"),
    path("estadisticas/anual/sales/price/payment-success/<int:year>/<str:product>/<str:product2>/<str:product3>/", payment_product_success_price_chart, name="product-anual-payment-success-price"),
    # cant month
    path("estadisticas/day/sales/<int:month>/<int:monthYear>/<str:monthproduct>/<str:monthproduct2>/<str:monthproduct3>/", get_day_sales_chart, name="product-day-sales-cant"),
    path("estadisticas/month/spend-per-customer/<int:month>/<int:monthYear>/<str:monthproduct>/<str:monthproduct2>/<str:monthproduct3>/", spend_month_per_customer_chart, name="product-month-spend-per-customer-cant"),
    path("estadisticas/month/payment-success/<int:month>/<int:monthYear>/<str:monthproduct>/<str:monthproduct2>/<str:monthproduct3>/", payment_month_success_chart, name="product-month-payment-success-cant"),
    # price month
    path("estadisticas/day/price/sales/<int:month>/<int:monthYear>/<str:monthproduct>/<str:monthproduct2>/<str:monthproduct3>/", get_day_sales_price_chart, name="product-day-price-sales"),
    path("estadisticas/month/price/spend-per-customer/<int:month>/<int:monthYear>/<str:monthproduct>/<str:monthproduct2>/<str:monthproduct3>/", spend_month_per_customer_price_chart, name="product-month-price-spend-per-customer"),
    path("estadisticas/month/price/payment-success/<int:month>/<int:monthYear>/<str:monthproduct>/<str:monthproduct2>/<str:monthproduct3>/", payment_month_success_price_chart, name="product-month-price-payment-success"),
    # Wharehouses
    path('reportes-de-almacenes/',reports_warehouses_view,name='reports_warehouses_view'),
    path('reportes-de-almacenes-movimientos-stock/<int:pk>',reports_warehouses_stock_movement_view,name='reports_warehouses_stock_movement_view'),
    path('reportes-de-almacenes-movimientos-stock-principal/<int:pk>',reports_warehouses_stock_principal_movement_view,name='reports_warehouses_stock_principal_movement_view'),
    
    
]