from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Continent)


class TickerAdmin(admin.ModelAdmin):
    list_display = ['name','long_name']
    search_fields = ['name','long_name']

class CountrieAdmin(admin.ModelAdmin):
    list_display = ['name','continent']
    search_fields = ['name']

class PriceAdmin(admin.ModelAdmin):
    list_display = ['ticker','date','value','country','continent']
    search_fields = ['ticker','country']
    ordering = ['continent','country','ticker','date']

admin.site.register(Ticker,TickerAdmin)
admin.site.register(Contrie,CountrieAdmin)
admin.site.register(Price,PriceAdmin)
