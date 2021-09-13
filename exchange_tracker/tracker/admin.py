from django.contrib import admin
from .models import *


class IndexPriceAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'value']
    search_fields = ['name']
    ordering = ['name', 'date']


class SectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'country_index']
    search_fields = ['name']


class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name', 'sector', 'country_index']
    search_fields = ['name']


class TIckerAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'sector', 'country_index']
    search_fields = ['name', 'industry', 'sector', 'country_index']


class TickerPriceAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'date', 'price',
                    'volume', 'change']
    search_fields = ['ticker']
    ordering = ['ticker', 'date']


# Register your models here.
admin.site.register(CountryIndex)
admin.site.register(IndexPrice, IndexPriceAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Ticker, TIckerAdmin)
admin.site.register(TickerPrice, TickerPriceAdmin)
