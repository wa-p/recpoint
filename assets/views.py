from django.shortcuts import render,redirect
from shipments.models import *
from recpoint.users.models import *
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Sum
from datetime import date
# Create your views here.




def driverPaymentTemplate(request):
		
	return render(request, "assets/new_action.html", {'form':FormDriverPayment})



def driverUnpaidOrders(request):
	#import pdb;   pdb.set_trace()
	if request.method == 'POST':
		shipments = Shipment.objects.filter(payed_driver=False,driver=request.POST['driver'])
		driver = User.objects.get(id=request.POST['driver'])
		s_total= Shipment.objects.filter(payed_driver=False,driver=request.POST['driver']).values('payed_miles','cost')
		total = 0
		for s in s_total:
			total = float(s['payed_miles'])*float(s['cost']) + total

	return render(request,'assets/driver_unpaid.html',{'orders':shipments,'driver':driver,'total':float(total*0.3)})


def driverPaymentResume(request):
	#import pdb;   pdb.set_trace()
	if request.method == 'POST':
		today = str(date.today())
		count = 0
		user = ""
		for k in request.POST.keys():
			if k.split('-')[0] == 'shipment':
				shipment = Shipment.objects.get(id=k.split('-')[1])
				shipment.payed_driver_date = today
				shipment.payed_driver = True
				shipment.save()
				count +=1
				user=shipment.driver.username


		messages.success(request, 'You have just payed '+ str(count) +' shipments to driver '+user) 
	return redirect('/assets/driverpayment/')
	#return render(request,'assets/driver_unpaid.html',{'orders':shipments,'driver':driver,'total':float(total*0.3)})


def driverPaymentOrders(request):
	#import pdb;   pdb.set_trace()
	if request.method == 'POST':
		shipments = Shipment.objects.filter(payed_driver=False,driver=request.POST['driver'])
		driver = User.objects.get(id=request.POST['driver'])
		s_total= Shipment.objects.filter(payed_driver=False,driver=request.POST['driver']).values('payed_miles','cost')
		total = 0
		for s in s_total:
			total = float(s['payed_miles'])*float(s['cost']) + total

	return render(request,'assets/driver_unpaid.html',{'orders':shipments,'driver':driver,'total':float(total*0.3)})
		#return redirect(DriverPaymentOrders)

def galPerMiles(request):
	#import pdb;   pdb.set_trace()
	if request.method=='POST':
		shipments = Shipment.objects.filter(end_miles__gt=0,order_date__range=[request.POST['start_date'], request.POST['end_date']]).order_by('-order_date')
		expenses_sum = ShipmentCost.objects.filter(expense_type='Gas').values('order_number').annotate(total=Sum('gas_gallons'))
	else:	
		shipments = Shipment.objects.filter(end_miles__gt=0).order_by('-order_date')
		expenses_sum = ShipmentCost.objects.filter(expense_type='Gas').values('order_number').annotate(total=Sum('gas_gallons'))
	

	return render(request,'assets/gal_miles.html',{'orders':shipments,'expenses_sum':expenses_sum,'type':'gallons'})


def dolarPerMiles(request):
	#import pdb;   pdb.set_trace()
	if request.method=='POST':
		shipments = Shipment.objects.filter(end_miles__gt=0,order_date__range=[request.POST['start_date'], request.POST['end_date']]).order_by('-order_date')
		expenses_sum = ShipmentCost.objects.all().values('order_number').annotate(total=Sum('cost'))
	else:	
		shipments = Shipment.objects.filter(end_miles__gt=0).order_by('-order_date')
		expenses_sum = ShipmentCost.objects.all().values('order_number').annotate(total=Sum('cost'))
	#expenses = ShipmentCost.objects.filter(expense_type='Gas').annotate(total=Sum('gas_gallons'))
	#import pdb;   pdb.set_trace()
		#shipments = Shipment.objects.filter(payed_driver=False,driver=request.POST['driver'])
		#driver = User.objects.get(id=request.POST['driver'])
	return render(request,'assets/gal_miles.html',{'orders':shipments,'expenses_sum':expenses_sum,'type':'dollar'})



def payedRealMiles(request):
	#import pdb;   pdb.set_trace()
	if request.method=='POST':
		shipments = Shipment.objects.filter(end_miles__gt=0,order_date__range=[request.POST['start_date'], request.POST['end_date']]).order_by('-order_date')
		#expenses_sum = ShipmentCost.objects.filter(expense_type='Gas').values('order_number').annotate(total=Sum('gas_gallons'))
	else:	
		shipments = Shipment.objects.filter(end_miles__gt=0).order_by('-order_date')
		#expenses_sum = ShipmentCost.objects.filter(expense_type='Gas').values('order_number').annotate(total=Sum('gas_gallons'))
	
	return render(request,'assets/diff_miles.html',{'orders':shipments})