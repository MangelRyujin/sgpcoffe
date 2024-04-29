from django.urls import path

from apps.reportes.views import reports_view



urlpatterns = [
    path('estadisticas/',reports_view,name='estadisticas'),
]