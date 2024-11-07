from django.urls import path
from apps.barandkitchen.views.bar_and_kitchen_views import *
from apps.barandkitchen.views.items_list_bar_and_kitchen_views import elaboration_items, items_list_bar_view, items_list_kitchen_view
from apps.barandkitchen.views.items_change_state_kitchen_and_bar import items_change_kitchen_view,items_change_bar_view,items_finish_bar_and_kitchen_view


urlpatterns = [
    # Prueba GET
    path('elaboracion/',bar_and_kitchen_elaboration_items,name='bar_and_kitchen_elaboration_items'),
    path('bar_and_kitchen_ordenado/',bar_and_kitchen_ordenado,name='bar_and_kitchen_ordenado'),
    path('items_proccess_view/<int:pk>/',items_proccess_view,name='items_proccess_view'),
    path('items_finish_view/<int:pk>/',items_finish_view,name='items_finish_view'),
    
    # Actual
    path('pedidos/',elaboration_items,name='kitchen_and_launch'),
    path('items/bar/',items_list_bar_view,name='items_list_bar'),
    path('items/kitchen/',items_list_kitchen_view,name='items_list_kitchen'),
    path('items/change/kitchen/',items_change_kitchen_view,name='items_change_kitchen'),
    path('items/change/bar/',items_change_bar_view,name='items_change_bar'),
    path('items/finished/',items_finish_bar_and_kitchen_view,name='items_finished_bar_and_kitchen'),
]