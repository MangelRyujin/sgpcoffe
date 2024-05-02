from django.shortcuts import render
from django.contrib.auth.decorators import login_required 

@login_required(login_url='admin/login/')
def example_view(request):
    return render(request,'example.html')