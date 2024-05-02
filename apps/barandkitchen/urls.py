from django.urls import path
from apps.barandkitchen.views.items_list_bar_and_kitchen_views import items_list_bar_and_kitchen_view


urlpatterns = [
    path('pedidos/',items_list_bar_and_kitchen_view,name='items_list_bar_and_kitchen'),
]