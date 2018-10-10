from django.conf.urls import url
from .views import *


app_name = "shipments"
urlpatterns = [
    url(r'^new-shipment/$', newShipment, name='newShipment'),
    url(r'^new-expense/$', newExpense, name='newExpense'),    
    

   
]
