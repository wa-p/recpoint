from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.http import QueryDict
from django.db.models import Sum
from django.contrib.auth.middleware import get_user


# Create your views here.



def newShipment(request):
	#import pdb;   pdb.set_trace()

	if request.method=='POST':
		form = FormShipment(request.POST, request.FILES)
		shipment = form.save(commit=False)
		try:
			cost = Cost.objects.get(shipment_type=request.POST['shipment_type'],company=request.POST['provider_company'])
			shipment.cost = cost.amount
			shipment.driver_1 = request.user
			shipment.save()
			messages.success(request, 'You have just created a New Shipment Order') 
		except Exception as e:
			#import pdb;   pdb.set_trace()
			messages.error(request, e) 
		
		
		
	return render(request, "shipments/new_action.html", {'form':FormShipment,'action':' SHIPMENT'})


def newExpense(request):
	#import pdb;   pdb.set_trace()
	
	if request.method=='POST':
		form = FormShipmentCost(request.user, request.POST)
		shipmentcost = form.save()
		if shipmentcost.expense_type == 'Gas':
			if shipmentcost.cost > 500:
				print('GAS TOO EXPENSIVE')
		elif shipmentcost.expense_type == 'Toll':
			if shipmentcost.cost > 30:
				print('TOLL TOO EXPENSIVE')
		elif shipmentcost.expense_type == 'Extra':
			if shipmentcost.cost > 200:
				print('EXTRA TOO EXPENSIVE')
		messages.success(request, 'You have just loaded a New Expense') 

	
	return render(request, "shipments/new_action.html", {'form':FormShipmentCost(request.user),'action':' EXPENSE'})


def lastExpense(request):
	#import pdb; pdb.set_trace()
	
	if request.method=='POST':
		form = FormLastShipmentCost(request.user, request.POST)
		shipmentcost = form.save()
		shipment = Shipment.objects.get(order_number=request.POST['order_number'])
		shipment.lastExpense = True
		shipment.save()
		if shipmentcost.expense_type == 'Gas':
			if shipmentcost.cost > 500:
				print('GAS TOO EXPENSIVE')
		elif shipmentcost.expense_type == 'Toll':
			if shipmentcost.cost > 30:
				print('TOLL TOO EXPENSIVE')
		elif shipmentcost.expense_type == 'Extra':
			if shipmentcost.cost > 200:
				print('EXTRA TOO EXPENSIVE')
		messages.success(request, 'You have just loaded a Last Expense') 

	
	return render(request, "shipments/new_action.html", {'form':FormLastShipmentCost(request.user),'action':' EXPENSE'})


def newPayment(request):
	#
	
	if request.method=='POST':
		form = FormPayment(request.POST,request.FILES)
		payment = form.save()
		shipment = Shipment.objects.get(id = request.POST['order_number'])
		if payment.payed_amount == shipment.cost*shipment.payed_miles:
			messages.success(request,'Shipment payment have been reconciled')
			shipment.payed = True
			shipment.reconcile = True
			shipment.check_amount = payment.payed_amount
			shipment.save()
			messages.success(request, 'You have just loaded a New Payment')			
		else:
			messages.warning(request,'Remember to load shipment payments variations')			
			shipment.payed = True			
			shipment.save()
			request.session['payment']=Payment.objects.get(order_number=request.POST['order_number']).id
			return redirect('shipments:variationLoad')
		#shipment.save()
		

	
	return render(request, "shipments/new_action.html", {'form':FormPayment,'action':' PAYMENT'})


def shipmentsList(request,option):
	total = 0
	expenses = 0
	expense_unit =""
	if option == 'open':
		if request.user.groups.filter(name='Management').exists():
			shipments = Shipment.objects.filter(end_miles=0)	
		elif request.user.groups.filter(name='Driver').exists():
			shipments = Shipment.objects.filter(end_miles=0,driver=request.user)
	elif option == 'all':
		if request.method=='POST':
			if request.user.groups.filter(name='Management').exists():
				shipments = Shipment.objects.filter(order_date__range=[request.POST['start_date'], request.POST['end_date']]).order_by('-order_date')	
			elif request.user.groups.filter(name='Driver').exists():
				shipments = Shipment.objects.filter(driver=request.user)
		else:
			if request.user.groups.filter(name='Management').exists():
				shipments = Shipment.objects.all().order_by('-order_date')
			elif request.user.groups.filter(name='Driver').exists():
				shipments = Shipment.objects.filter(driver=request.user)
	elif option == 'closed':
		if request.POST:
			shipments = Shipment.objects.filter(end_miles__gt=0,payed=False,delivery_date__range=[request.POST['start_date'], request.POST['end_date']])	
			#shipments = Payment.objects.filter(payment_date__range=[request.POST['start_date'], request.POST['end_date']]).order_by('-payment_date')
		else:	
			shipments = Shipment.objects.filter(end_miles__gt=0,payed=False)	
			#shipments = Payment.objects.all().order_by('-payment_date')
		for e in shipments:
				total = e.payed_driver + total
	elif option == 'client':
		if request.POST:
			#shipments = Shipment.objects.filter(payed=True,delivery_date__range=[request.POST['start_date'], request.POST['end_date']])	
			shipments = Payment.objects.filter(payment_date__range=[request.POST['start_date'], request.POST['end_date']]).order_by('-payment_date')
		else:	
			#shipments = Shipment.objects.filter(payed_driver=True)	
			shipments = Payment.objects.all().order_by('-payment_date')
	elif option == 'driver':
		if request.POST:
			shipments = Shipment.objects.filter(Q(payed_driver_1=True,delivery_date__range=[request.POST['start_date'], request.POST['end_date']])|Q(payed_driver_2=True,delivery_date__range=[request.POST['start_date'], request.POST['end_date']]))	
			#shipments = Payment.objects.filter(payment_date__range=[request.POST['start_date'], request.POST['end_date']]).order_by('-payment_date')
		else:	
			shipments = Shipment.objects.filter(Q(payed_driver_1=True)|Q(payed_driver_2=True))	
			#shipments = Payment.objects.all().order_by('-payment_date')
		for e in shipments:
			if e.tandem:
				total = e.check_amount*0.15 + total
			else:
				total = e.check_amount*0.3 + total
	elif option == 'expense':
		if request.POST:
			s_values = Shipment.objects.filter(payed=True,order_date__range=[request.POST['start_date'], request.POST['end_date']]).order_by('-order_date').values_list('id',flat=True)
			shipments = Payment.objects.filter(order_number__in=s_values).order_by('-payment_date')
			expenses = ShipmentCost.objects.filter(order_number__in=s_values).aggregate(Sum("cost"))
			#import pdb; pdb.set_trace()
		else:
			shipments = Payment.objects.all().order_by('-payment_date')		
			expenses = ShipmentCost.objects.aggregate(Sum("cost"))
		expense_unit = ShipmentCost.objects.all().values('order_number').annotate(total=Sum('cost'))
		for e in shipments:
				total = e.payed_amount + total


	
	return render(request,'shipments/shipments_list.html',{'shipments':shipments,'option':option,'total':total,'expenses':expenses,'expense_unit':expense_unit})


def shipmentsClose(request,idorder):
	order = Shipment.objects.get(id=idorder)
	if request.method=='POST':
		#form = FormShipmentClose(request.POST,request.FILES)
		
		#
		order.end_miles = request.POST['end_miles']
		order.delivery_date = request.POST['delivery_date']
		order.order_picture = request.FILES['order_picture']
		if float(order.end_miles) <= order.start_miles:
			messages.error(request, 'Error on End Miles.. Value must be greater than Starting Miles') 	
		else:
			messages.success(request, 'You have just closed order number: '+ order.order_number) 	
			order.save()
			return redirect('/shipments/list-shipments/open/')
		

	
	return render(request, "shipments/shipments_close.html", {'form':FormShipmentClose,'order':order.order_number})


def expenseList(request,idorder):
	order = Shipment.objects.get(id=idorder)
	gas_expenses = ShipmentCost.objects.filter(order_number=order,expense_type='Gas')
	toll_expenses = ShipmentCost.objects.filter(order_number=order,expense_type='Toll')
	def_expenses = ShipmentCost.objects.filter(order_number=order,expense_type='Def')
	extra_expenses = ShipmentCost.objects.filter(order_number=order,expense_type='Extra')
	total = ShipmentCost.objects.filter(order_number=idorder).aggregate(Sum("cost"))
	gas_total = ShipmentCost.objects.filter(order_number=idorder,expense_type='Gas').aggregate(Sum("cost"))
	toll_total = ShipmentCost.objects.filter(order_number=idorder,expense_type='Toll').aggregate(Sum("cost"))
	def_total = ShipmentCost.objects.filter(order_number=idorder,expense_type='Def').aggregate(Sum("cost"))
	extra_total = ShipmentCost.objects.filter(order_number=idorder,expense_type='Extra').aggregate(Sum("cost"))

	context = {'gas_expense':gas_expenses,
				'toll_expense':toll_expenses,
				'def_expense':def_expenses,
				'extra_expense':extra_expenses,
				'total':total,
				'gas_total':gas_total,
				'toll_total':toll_total,
				'def_total':def_total,
				'extra_total':extra_total,
				'order':order}

	return render(request, "shipments/expense_detail.html", context)


def shipmentDetail(request,idorder):
	order = Shipment.objects.get(id=idorder)
	expenses = ShipmentCost.objects.filter(order_number=order)
	#total = ShipmentCost.objects.filter(order_number=idorder).aggregate(Sum("cost"))

	return render(request, "shipments/shipment_detail.html", {'expenses':expenses,'shipment':order})


def variationSelect(request):
	if request.method=='POST':
		#import pdb;   pdb.set_trace()
		request.session['payment']=Payment.objects.get(order_number=request.POST['order_number']).id
		return redirect('shipments:variationLoad')
	return render(request, "shipments/new_action.html", {'form':FormVariationSelect})


def variationLoad(request):
	#order = Shipment.objects.get()
	#
	
	if request.method=='POST':
		s = Payment.objects.get(id=request.session['payment'])
		form = FormVariationLoad(request.POST,request.FILES)
		variation = form.save(commit=False)
		variation.payment_number = s
		variation.save();


	s = Payment.objects.get(id=request.session['payment'])
	variations = PaymentVariation.objects.filter(payment_number=request.session['payment'])
	total_deduction = PaymentVariation.objects.filter(payment_number=request.session['payment'],variation_type='Deduction').aggregate(Sum("amount"))
	total_bonus = PaymentVariation.objects.filter(payment_number=request.session['payment'],variation_type='Bonus').aggregate(Sum("amount"))
	#import pdb;   pdb.set_trace()
	if total_bonus['amount__sum']==None:
		total_bonus['amount__sum']=0.0

	if total_deduction['amount__sum']==None:
		total_deduction['amount__sum']=0.0

	total_variation = float(total_bonus['amount__sum']) - float(total_deduction['amount__sum'])
	
	final_payment =  s.payed_amount - total_variation
	#import pdb; pdb.set_trace()
	if final_payment == Shipment.objects.get(order_number=s.order_number.order_number).payed_miles*Shipment.objects.get(order_number=s.order_number.order_number).cost:
		messages.success(request, 'Order '+s.order_number.order_number +' Reconciled') 
		s.order_number.check_amount = s.payed_amount
		s.order_number.reconcile = True
		s.order_number.save()
		return redirect('shipments:variationSelect')
	else:
		#
		messages.error(request, 'Not Reconciled') 
		#return render(request, "shipments/variation_load.html", {'form':FormVariationLoad,'shipments':s})	
	return render(request, "shipments/variation_load.html", {'form':FormVariationLoad,'shipment':s,'variations':variations,'t_deduction':total_deduction,'t_bonus':total_bonus,'t_variation':total_variation})



def shipmentPictureSelect(request):
	if request.method=='POST':
		request.session['shipment']=request.POST['order_number']
		return redirect('shipments:shipmentPictureLoad')
	return render(request, "shipments/new_action.html", {'form':FormShipmentSelect})



def shipmentPictureLoad(request):
	
	if request.method=='POST':
		
		form = FormShipmentPicture(request.POST,request.FILES)
		file = form.save(commit=False)
		file.order_number = Shipment.objects.get(id=request.session['shipment'])
		file.save()
	
	picture = ShipmentPicture.objects.filter(order_number=Shipment.objects.get(id=request.session['shipment']))
	shipment = Shipment.objects.get(id=request.session['shipment'])
	return render(request, "shipments/shipmentPicture_load.html", {'form':FormShipmentPicture,'pictures':picture,'shipment':shipment})