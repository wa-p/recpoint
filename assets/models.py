from django.db import models
#from shipments.models import Payment
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Vehicle(models.Model):	

	TRAILER = 'Trailer'
	TRUCK = 'Truck'
	VEHICLE_TYPE = (
		(TRAILER, 'TRAILER'),
		(TRUCK, 'TRUCK')
	)


	OK = 'Ok'
	DAMAGED = 'Damaged'
	RETIRED = 'Retired'
	STATUS_TYPE = (
		(OK, 'OK'),
		(DAMAGED, 'DAMAGED'),
		(RETIRED, 'RETIRED')
	)

	vin_number = models.CharField(_("Vin Number"),blank=False,max_length=200)
	plate = models.CharField(_("Plate Number"),blank=False,max_length=200)
	vehicle_type = models.CharField(_("Vehicle Type"),blank=False, max_length=7,default='TRUCK', choices=VEHICLE_TYPE) #models.ForeignKey(Categoria)
	picture = models.ImageField(_("Vehicle Picture"), blank=True, null=True, max_length=200)
	purchase_date = models.DateField(_("Date of purchase"),blank=True)
	status = models.CharField(_("Status"),blank=False, max_length=7,default='OK', choices=STATUS_TYPE) #models.ForeignKey(Categoria)

	def __str__(self):
		return self.plate


class Maintenance(models.Model):

	REGULAR = 'Regular'
	FIX = 'Fix'
	MAINTENANCE_TYPE = (
		(REGULAR, 'REGULAR'),
		(FIX, 'FIX')
	)

	vehicle = models.ForeignKey(Vehicle,on_delete=models.PROTECT)
	maintenance_type = models.CharField(_("Maintenance Type"),blank=False, max_length=7,default='REGULAR', choices=MAINTENANCE_TYPE) #models.ForeignKey(Categoria)
	cost = models.FloatField(_("Maintenance Cost"), blank=False)
	maintenance_date = models.DateField(_("Maintenance Date"),blank=False)
	description = models.TextField(_("Maintenance Description"), blank=False)

	def __str__(self):
		return self.vehicle.plate


"""

class PaymentVariation(models.Model):
	BONUS = 'Bonus'
	DEDUCTION = 'Deduction'
	VARIATION_TYPE = (
			(BONUS,'BONUS'),
			(DEDUCTION,'DEDUCTION')
		)
	payment_number = models.ForeignKey(Payment,on_delete=models.PROTECT)
	variation_type = models.CharField(_("Variation Type"),blank=False, max_length=9,default='BONUS', choices=VARIATION_TYPE) #models.ForeignKey(Categoria)
	ammount = models.FloatField(_("Maintenance Cost"), blank=False)
	description = models.CharField(_("Description"),blank=False,max_length) #models.ForeignKey(Categoria)

	def __str__(self):
		return self.payment_number.id + " " +variation_type

"""