from django.urls import path
from apps.waiter.views.example import example_view, mesas, menu, notificaciones, barras


urlpatterns = [
    path('ejemplo/', example_view, name='example'),
    path('mesas/', mesas, name='mesas'),
    path('menu/', menu, name='menu'),
    path('notificaciones/', notificaciones, name='notificaciones'),
    path('barras/', barras, name='barras'),
]