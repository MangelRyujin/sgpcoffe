from django.urls import path
from apps.waiter.views.create_order_and_items import *
from apps.waiter.views.deliveryTable.list_order_item_delivery_delete import *
from apps.waiter.views.deliveryTable.list_orders_table import *
from apps.waiter.views.example import *
from apps.waiter.views.example_delete import *
from apps.waiter.views.item_process import *
from apps.waiter.views.print import *


urlpatterns = [
    # Get
    path('', example_view, name='example'),
    path('charge_table/<int:pk>/', charge_table, name='charge_table'),
    path('table_list_update_view/', table_list_update_view, name='table_list_update_view'),
    path('product_list_results/<int:pk>/', product_list_results, name='product_list_results'),
    path('order_items_result/<int:pk>/', order_items_result, name='order_items_result'),
    path('order_detail_view/<int:pk>/', order_detail_view, name='order_detail_view'),
    path('list_orders_table_view/<int:pk>/', list_orders_table_view, name='list_orders_table_view'),
    path('order_detail_delivery_table_view/<int:pk>/', order_detail_delivery_table_view, name='order_detail_delivery_table_view'),
    path('list_orders_table_result_view/<int:pk>/', list_orders_table_result_view, name='list_orders_table_result_view'),
    path('reload_order_sold_detail_delivery_table_view/<int:pk>/', reload_order_sold_detail_delivery_table_view, name='reload_order_sold_detail_delivery_table_view'),
    path('charge_delivery_table/<int:pk>/', charge_delivery_table, name='charge_delivery_table'),
    
    
    # Create
    path('order_create_view/<int:pk>/', order_create_view, name='order_create_view'),
    path('order_item_create_view/<int:pk>/', order_item_create_view, name='order_item_create_view'),
    path('order_item_add_create/<int:pk>/', order_item_add_create, name='order_item_add_create'),
    path('order_item_util_create/<int:pk>/', order_item_util_create, name='order_item_util_create'),
    path('order_create_delivery_view/<int:pk>/', order_create_delivery_view, name='order_create_delivery_view'),
    path('reload_order_detail_delivery_table_view/<int:pk>/', reload_order_detail_delivery_table_view, name='reload_order_detail_delivery_table_view'),
    path('order_item_add_message/<int:pk>/', order_item_add_message, name='order_item_add_message'),
    
    # Update
    path('order_change_table_form_view/<int:pk>/', order_change_table_form_view, name='order_change_table_form_view'),
    path('order_item_check_view/<int:pk>/', order_item_check_view, name='order_item_check_view'),
    path('order_item_revert_view/<int:pk>/', order_item_revert_view, name='order_item_revert_view'),
    path('order_item_cancel_view/<int:pk>/', order_item_cancel_view, name='order_item_cancel_view'),
    path('order_item_delivery_view/<int:pk>/', order_item_delivery_view, name='order_item_delivery_view'),
    path('order_sold/<int:pk>/', order_sold, name='order_sold'),
    path('order_change_table_delivery_form_view/<int:pk>/', order_change_table_delivery_form_view, name='order_change_table_delivery_form_view'),
    path('order_delivery_sold/<int:pk>/', order_delivery_sold, name='order_delivery_sold'),
    path('table_order_delivery_sold/<int:pk>/', table_order_delivery_sold, name='table_order_delivery_sold'),
    path('order_item_delivery_waiter_view/<int:pk>/', order_item_delivery_waiter_view, name='order_item_delivery_waiter_view'),
    path('order_item_check_all_view/<int:pk>/', order_item_check_all_view, name='order_item_check_all_view'),
    path('order_item_revert_all_view/<int:pk>/', order_item_revert_all_view, name='order_item_revert_all_view'),
    path('delivery_order_item_check_all_view/<int:pk>/', delivery_order_item_check_all_view, name='delivery_order_item_check_all_view'),
    path('delivery_order_item_revert_all_view/<int:pk>/', delivery_order_item_revert_all_view, name='delivery_order_item_revert_all_view'),
    
    
    # Delete
    path('order_item_delete_view/<int:pk>/', order_item_delete_view, name='order_item_delete_view'),
    path('order_delete_view/<int:pk>/', order_delete_view, name='hx_order_delete_view'),
    path('order_item_add_delete_view/<int:pk>/', order_item_add_delete_view, name='order_item_add_delete_view'),
    path('order_item_utils_delete_view/<int:pk>/', order_item_utils_delete_view, name='order_item_utils_delete_view'),
    path('order_delivery_delete_view/<int:pk>/', order_delivery_delete_view, name='order_delivery_delete_view'),
    path('order_detail_delivery_delete_view/<int:pk>/', order_detail_delivery_delete_view, name='order_detail_delivery_delete_view'),
    
    # Print
    path('get_products_print/<int:pk>/', get_products_print, name='get_products_print'),
    
    
    
]