from django.contrib import admin
from django.contrib.auth import admin as auth_admin
# Register your models here.
from .models import *


admin.site.register(State)
admin.site.register(ShipmentType)
admin.site.register(Shipment)
admin.site.register(Cost)
admin.site.register(PriceHistory)
admin.site.register(ShipmentCost)
admin.site.register(Payment)
admin.site.register(ShipmentCompany)
admin.site.register(PaymentVariation)
admin.site.register(ShipmentPicture)


# Register your models here.
class ShipmentAdmin(admin.ModelAdmin):
    ...
    search_fields = ['destination', 'driver', 'truck', 'shipment_type']