from django.urls import path
from apps.waiter.views.example import example_view


urlpatterns = [
    path('ejemplo/',example_view,name='example'),
]