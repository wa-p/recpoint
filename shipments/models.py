from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy as _
from assets.models import *
from recpoint.users.models import *
# Create your models here.


class State(models.Model):

	state = models.CharField(_('State Name'),blank=False,max_length=20)

	def __str__(self):
		return self.state


class ShipmentType(models.Model):

	value = models.CharField(_('Shipment Type'),blank=False, max_length=20)

	def __str__(self):
		return self.value


class Cost(models.Model):	

	

	#shipment_type = models.ForeignKey(ShipmentType,on_delete=models.PROTECT, unique=True)
	shipment_type = models.OneToOneField('ShipmentType', on_delete=models.PROTECT)
	ammount = models.FloatField(_("Ammount"),blank=False,max_length=15)
	
	

	def __str__(self):
		return self.shipment_type.value


class PriceHistory(models.Model):


	shipment_type = models.ForeignKey(ShipmentType,on_delete=models.PROTECT)
	ammount = models.FloatField(_("Ammount"),blank=False,max_length=15)
	start_date = models.DateField(_("Start Date"),blank=False)
	end_date = models.DateField(_("End Date"),default='2050-12-31')

	def __str__(self):
		return self.shipment_type.value + " " + self.end_date.strftime('%m/%d/%Y')


class Shipment(models.Model):

	order_number = CharField(_("Order Number"), blank=False, max_length=255, unique=True)
	provider_company = CharField(_("Provider Company"), blank=False,default="Vandyville", max_length=255,editable = False)
	destination = models.ForeignKey(State,on_delete=models.PROTECT,blank=False)
	order_date = models.DateField(_("Order Date"),blank=False)
	shipment_type = models.ForeignKey(ShipmentType,on_delete=models.PROTECT,blank=False)
	cost = models.FloatField(_('Cost by mile'),blank=False, default=0)
	payed_miles = models.FloatField(_("Payed Miles"),blank=False,max_length=15)
	start_miles = models.FloatField(_("Starting Miles"),blank=True, default=0,max_length=15)
	end_miles = models.FloatField(_("Ending Miles"),blank=True, default=0 ,max_length=15)
	delivery_date = models.DateField(_("Delivery Date"),blank=True,null=True)
	driver = models.ForeignKey(User,on_delete=models.PROTECT,blank=True, null=True)
	truck = models.ForeignKey(Vehicle,on_delete=models.PROTECT,blank=True,related_name='truck',null=True)
	trailer = models.ForeignKey(Vehicle,on_delete=models.PROTECT,blank=True,related_name='trailer',null=True)
	payed = models.BooleanField(_("Has been payed?"),default=False)

	def __str__(self):
		return self.order_number


class ShipmentCost(models.Model):

	TOLL = 'Toll'
	GAS = 'Gas'
	EXPENSE_OPTION = (
        (TOLL, 'Toll'),
        (GAS, 'Gas'),
        )

	order_number = models.ForeignKey(Shipment,on_delete=models.PROTECT,blank=False)
	expense_type = models.CharField(_('Expense Type'),max_length=4, blank=False, default='Gas', choices=EXPENSE_OPTION)
	gas_gallons = models.FloatField(_("Gas Gallons"),blank=False,default=0,max_length=10)
	cost = models.FloatField(_("Total Payed"),blank=False, default=0,max_length=10)
	#highlight = models.BooleanField(_("Did something went wrong?"),default=False)
	#description = models.TextField(_("Describe what went wrong"), blank=True)
	

	def __str__(self):
		return self.order_number.order_number