"""
URL configuration for coffee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

from coffee.views.home_view import home_view

# Registrar la vista en urls.py
urlpatterns = [
    
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view,name='home'),
    path('reportes/',include("apps.reportes.urls"))
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns+=[
    re_path(r'^media/(?P<path>.*)$',serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]
