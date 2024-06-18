from django.contrib import admin
from .models import Coin
from solo.admin import SingletonModelAdmin

# Register your models here.
admin.site.register(Coin, SingletonModelAdmin)
