from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse

@login_required(login_url='admin/login/')
def example_view(request):
    print('example')
    return render(request,'mesero/example.html')

@login_required(login_url='admin/login/')
def mesas(request):
    return render(request, 'mesero/partials/mesas.html')

@login_required(login_url='admin/login/')
def menu(request):
    return render(request, 'mesero/partials/menu.html')

@login_required(login_url='admin/login/')
def notificaciones(request):
    return HttpResponse('''<div class="flex items-center justify-center">
    <h1 class="mx-auto w-full mt-3 text-2xl text-white font-semibold text-center">
        Notificaciones
    </h1>
</div>''')

@login_required(login_url='admin/login/')
def barras(request):
    return HttpResponse('''<div>
    <h1 class="mx-auto mt-3 text-2xl text-white font-semibold text-center">
        Barras
    </h1>
</div>''')