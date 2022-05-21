from django.contrib import admin
from .models import *


class AdvisorAdmin(admin.ModelAdmin):
    list_display = ["advisorid", "advisor", "is_active"]
    search_fields = ["advisorid"]
    ordering = ["advisorid"]


class ClientAdmin(admin.ModelAdmin):
    list_display = ["clientid", "name", "client_type", "is_active"]
    search_fields = ["clientid"]
    ordering = ["clientid"]


class AccountTypeAdmin(admin.ModelAdmin):
    search_fields = ["account_type"]
    ordering = ["account_type"]


class AccountAdmin(admin.ModelAdmin):
    list_display = ["accountid", "clientid", "account_type"]
    search_fields = ["accountid", "clientid"]
    ordering = ["accountid", "clientid"]


class SecurityAssetClassAdmin(admin.ModelAdmin):
    search_fields = ["security_asset_class"]
    ordering = ["security_asset_class"]


class SecurityAdmin(admin.ModelAdmin):
    list_display = ["securityid", "name", "asset_class"]
    search_fields = ["securityid"]
    ordering = ["securityid"]


class SecurityPriceAdmin(admin.ModelAdmin):
    list_display = ["securityid", "date", "price"]
    search_fields = ["securityid"]
    ordering = ["securityid", "date"]


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "accountid",
        "security",
        "trade_date",
        "trx_type",
        "trx_amt",
        "trx_qty",
    ]
    search_fields = ["accountid", "securityid", "trx_type"]
    ordering = ["accountid", "security", "trade_date"]


class PositionAdmin(admin.ModelAdmin):
    list_display = ["account", "security", "date", "mv"]
    search_fields = ["account", "security", "date"]
    ordering = ["account", "security", "date"]


# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(SecurityAssetClass, SecurityAssetClassAdmin)
admin.site.register(Security, SecurityAdmin)
admin.site.register(SecurityPrice, SecurityPriceAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(Position, PositionAdmin)
