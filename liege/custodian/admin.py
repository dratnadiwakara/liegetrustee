from django.contrib import admin
from django.apps import apps
from custodian.models import *

admin.site.register(EquityTrade)
admin.site.register(EquityHolding)
admin.site.register(ListedEquity)
admin.site.register(StockBroker)
admin.site.register(MarginAccount)
admin.site.register(CDSAccount)
admin.site.register(Client)
admin.site.register(ClientBalance)

@admin.register(CustodyClient)
class CustodyClientAdmin(admin.ModelAdmin):
    pass

