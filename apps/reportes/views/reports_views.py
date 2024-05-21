from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.cuentas.models import Item,  Shift
from utils.validates.validate_date import validate_dates

@login_required(login_url='/admin/login/')
def reports_view(request):
    
    return render(request, "reports.html", {})

  
