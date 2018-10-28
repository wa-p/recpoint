from django.conf.urls import url
from .views import *


app_name = "shipments"
urlpatterns = [
    url(r'^new-shipment/$', newShipment, name='newShipment'),
    url(r'^new-expense/$', newExpense, name='newExpense'),  
    url(r'^last-expense/$', lastExpense, name='lastExpense'),  
    url(r'^new-payment/$', newPayment, name='newPayment'),  
    url(r'^list-shipments/(?P<option>[a-z]+)/$', shipmentsList, name='shipmentsList'),    
    url(r'^close-shipments/(?P<idorder>[0-9]+)/$', shipmentsClose, name='shipmentsClose'),    
    url(r'^expense-detail/(?P<idorder>[0-9]+)/$', expenseList, name='expenseList'),    
    url(r'^shipment-detail/(?P<idorder>[0-9]+)/$', shipmentDetail, name='shipmentDetail'),    
   
]
