from django.db import models
from datetime import datetime   
# Create your models here.

from django.utils.translation import ugettext_lazy as _
from recpoint.users.models import *
from assets.models import *
# Create your models here.


class State(models.Model):

	state = models.CharField(_('State Name'),blank=False,max_length=20)

	def __str__(self):
		return self.state

class ShipmentCompany(models.Model):

	name = models.CharField(_('Company Name'),blank=False, max_length=100)

	def __str__(self):
		return self.name


class ShipmentType(models.Model):

	value = models.CharField(_('Shipment Type'),blank=False, max_length=20)

	def __str__(self):
		return self.value


class Cost(models.Model):	

	
	company = models.ForeignKey(ShipmentCompany,on_delete=models.PROTECT, default=1)
	#shipment_type = models.ForeignKey(ShipmentType,on_delete=models.PROTECT, unique=True)
	shipment_type = models.ForeignKey(ShipmentType,on_delete=models.PROTECT)
	amount = models.FloatField(_("Amount"),blank=False,max_length=15,default=0)
	
	

	def __str__(self):
		return self.shipment_type.value +" "+ self.company.name


class PriceHistory(models.Model):


	shipment_type = models.ForeignKey(ShipmentType,on_delete=models.PROTECT)
	amount = models.FloatField(_("Amount"),blank=False,max_length=15, default=0)
	start_date = models.DateField(_("Start Date"),blank=False)
	end_date = models.DateField(_("End Date"),default='2050-12-31')

	def __str__(self):
		return self.shipment_type.value + " " + self.end_date.strftime('%m/%d/%Y')


class Shipment(models.Model):

	order_number = CharField(_("Order Number"), blank=False, max_length=255, unique=True)
	provider_company = models.ForeignKey(ShipmentCompany,on_delete=models.PROTECT,blank=False,default=1)
	#CharField(_("Provider Company"), blank=False,default="Vandyville", max_length=255,editable = False)
	destination = models.ForeignKey(State,on_delete=models.PROTECT,blank=False)
	order_date = models.DateField(_("Order Date"),blank=False)
	shipment_type = models.ForeignKey(ShipmentType,on_delete=models.PROTECT,blank=False)
	cost = models.FloatField(_('Cost by mile'),blank=False, default=0)
	payed_miles = models.FloatField(_("Payed Miles"),blank=False,max_length=15)
	start_miles = models.FloatField(_("Starting Miles"),blank=False,max_length=15)
	end_miles = models.FloatField(_("Ending Miles"),blank=True, default=0 ,max_length=15)
	delivery_date = models.DateField(_("Delivery Date"),blank=True,null=True)
	driver_1 = models.ForeignKey(User,on_delete=models.PROTECT,blank=True, null=True,related_name='driver_1')
	driver_2 = models.ForeignKey(User,on_delete=models.PROTECT,blank=True, null=True,related_name='driver_2')
	truck = models.ForeignKey(Vehicle,on_delete=models.PROTECT,blank=True,related_name='truck',null=True)
	trailer = models.ForeignKey(Vehicle,on_delete=models.PROTECT,blank=True,related_name='trailer',null=True)
	payed = models.BooleanField(_("Payed by client?"),default=False)
	payed_driver_1 = models.BooleanField(_("Payed to Driver 1?"),default=False)
	payed_driver_2 = models.BooleanField(_("Payed to Driver 2?"),default=False)
	order_picture = models.ImageField( blank=True, null=True, max_length=200)
	payed_driver_1_date = models.DateField(_("Driver 1 Payment Date"),blank=True,null=True)
	payed_driver_2_date = models.DateField(_("Driver 2 Payment Date"),blank=True,null=True)
	tandem = models.BooleanField(_("Team drivers?"),default=False)
	last_expense = models.BooleanField(_("Last expense loaded?"),default=False)
	check_amount = models.FloatField(_('Check Amount'),blank=False, default=0)
	reconcile = models.BooleanField(_("Reconciled acount?"),default=False)

	def __str__(self):
		return self.order_number

	def driver_payment(self):
		if self.tandem:
			return self.check_amount/2
		else:
			return self.check_amount
		

	def order_payment(self):
		return self.payed_miles * self.cost

	def real_miles(self):
		return self.end_miles - self.start_miles

	def diff_miles(self):
		return float(self.payed_miles - self.end_miles + self.start_miles)



class ShipmentCost(models.Model):

	TOLL = 'Toll'
	DEF = 'Def'
	GAS = 'Gas'
	EXTRA = 'Extra'
	EXPENSE_OPTION = (
        (TOLL, 'Toll'),
        (GAS, 'Gas'),
        (EXTRA,'Extra'),
        (DEF,'Def')
        )

	order_number = models.ForeignKey(Shipment,on_delete=models.PROTECT,blank=False)
	expense_type = models.CharField(_('Expense Type'),max_length=5, blank=False, default='Gas', choices=EXPENSE_OPTION)
	gas_gallons = models.FloatField(_("Gas Gallons"),blank=False,default=0,max_length=10)
	cost = models.FloatField(_("Total Payed"),blank=False, default=0,max_length=10)
	description = models.TextField(_("Describe what went wrong"), blank=True)
	

	def __str__(self):
		return self.order_number.order_number


class Payment(models.Model):
	order_number = models.ForeignKey(Shipment,on_delete=models.PROTECT,blank=False)
	payed_amount = models.FloatField(_("Payed Amount"),blank=False,max_length=15,default=0)
	check_number = CharField(_("Check Number"), blank=True, max_length=255, unique=True)
	payment_date =  models.DateField(_("Payment Date"),blank=False)
	payment_picture = models.ImageField( blank=True, null=True, max_length=200)

	def __str__(self):
		return self.order_number.order_number


class PaymentVariation(models.Model):
	BONUS = 'Bonus'
	DEDUCTION = 'Deduction'
	VARIATION_TYPE = (
			(BONUS,'BONUS'),
			(DEDUCTION,'DEDUCTION')
		)
	payment_number = models.ForeignKey(Payment,on_delete=models.PROTECT)
	variation_type = models.CharField(_("Variation Type"),blank=False, max_length=9,default='BONUS', choices=VARIATION_TYPE) #models.ForeignKey(Categoria)
	amount = models.FloatField(_("Variation Amount"), blank=False,default=0)
	description = models.CharField(_("Description"),blank=False,max_length=100) 

	def __str__(self):
		return self.variation_type + " " +self.payment_number.order_number.order_number



class ShipmentPicture(models.Model):
	order_number = models.ForeignKey(Shipment,on_delete=models.PROTECT,blank=False)
	picture = models.ImageField( blank=True, null=True, max_length=200)
	date =  models.DateField(_("Upload Date"),blank=True,default=datetime.now)

	def __str__(self):
		return self.order_number.order_number + " " + str(self.id)