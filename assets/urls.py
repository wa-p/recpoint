from django.conf.urls import url
from .views import *


app_name = "assets"
urlpatterns = [
    url(r'^driverpayment/$', driverPaymentTemplate, name='driverPayment'),
    url(r'^driverunpaidorder/$', driverUnpaidOrders, name='driverUnpaidOrders'),
    url(r'^driverpaidresume/$', driverPaymentResume, name='driverPaymentResume'),
    url(r'^galpermiles/$', galPerMiles, name='galPerMiles'),
    url(r'^dolarpermiles/$', dolarPerMiles, name='dolarPerMiles'),
    url(r'^payedrealmiles/$', payedRealMiles, name='payedRealMiles'),

]
