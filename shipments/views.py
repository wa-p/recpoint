from django.shortcuts import render
from .forms import *
from django.contrib import messages
from .models import *

# Create your views here.

def newShipment(request):
	#import pdb;   pdb.set_trace()

	if request.method=='POST':
		form = FormShipment(request.POST, request.FILES)
		shipment = form.save(commit=False)
		cost = Cost.objects.get(shipment_type=request.POST['shipment_type'])
		shipment.cost = cost.ammount
		shipment.save()
		messages.success(request, 'You have just created a New Shipment Order') 
	return render(request, "shipments/new_shipment.html", {'form':FormShipment})

def newExpense(request):
	#import pdb;   pdb.set_trace()
	
	if request.method=='POST':
		form = FormShipmentCost(request.POST, request.FILES)
		shipmentcost = form.save()
		messages.success(request, 'You have just loaded a New Expense') 

	
	return render(request, "shipments/new_expense.html", {'form':FormShipmentCost(user=request.user)})