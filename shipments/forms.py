from django import forms
from .models import *
from django.db.models import Q

class FormShipment(forms.ModelForm):

	class Meta:
		model = Shipment
		fields = ['order_number','provider_company','destination','order_date','shipment_type','payed_miles','start_miles','truck','trailer','tandem','driver_2']

	def __init__(self, *args, **kwargs):
		super(FormShipment, self).__init__(*args, **kwargs)
		self.fields['trailer'].queryset = Vehicle.objects.filter(vehicle_type='Trailer',status='Ok')
		self.fields['truck'].queryset = Vehicle.objects.filter(vehicle_type='Truck',status='Ok')
		#self.fields['driver_2'].widget = forms.HiddenInput()


class FormShipmentCost(forms.ModelForm):
    
	class Meta:
		model = ShipmentCost
		fields = '__all__'

	def __init__(self, user, *args, **kwargs):
		super(FormShipmentCost, self).__init__(*args, **kwargs)
		if User.objects.get(id=user.id).groups.filter(name='Management').exists():
			self.fields['order_number'].queryset = Shipment.objects.filter(end_miles=0).order_by('-order_date')	
		else:
			self.fields['order_number'].queryset = Shipment.objects.filter(Q(end_miles=0,driver_1=user)|Q(end_miles=0,driver_2=user)).order_by('-order_date')


class FormLastShipmentCost(forms.ModelForm):

	class Meta:
		model = ShipmentCost
		fields = '__all__'

	def __init__(self, user, *args, **kwargs):
		super(FormLastShipmentCost, self).__init__(*args, **kwargs)
		if user.groups.filter(name='Management').exists():
			self.fields['order_number'].queryset = Shipment.objects.filter(last_expense=False,end_miles__gt=0).order_by('-order_date')	
		else:
			self.fields['order_number'].queryset = Shipment.objects.filter(Q(last_expense=False,end_miles__gt=0,driver_1=user)|Q(last_expense=False,end_miles__gt=0,driver_2=user)).order_by('-order_date')

		self.fields['expense_type'].initial = ['Gas']
		self.fields['expense_type'].disabled = True

		


class FormPayment(forms.ModelForm):

	class Meta:
		model = Payment
		fields = '__all__'

	def __init__(self,  *args, **kwargs):
		super(FormPayment, self).__init__( *args, **kwargs)
		self.fields['order_number'].queryset = Shipment.objects.filter(payed=False,end_miles__gt=0)


class FormShipmentClose(forms.ModelForm):
    
	class Meta:
		model = Shipment
		fields = ['delivery_date','end_miles', 'order_picture']

	def __init__(self, *args, **kwargs):
		super(FormShipmentClose, self).__init__(*args, **kwargs)
		self.fields['delivery_date'].required = True
		self.fields['end_miles'].required = True
		self.fields['order_picture'].required = True
		self.fields['end_miles'].initial = ''


class FormVariationSelect(forms.ModelForm):

	class Meta:
		model = Payment
		fields = ['order_number']

	def __init__(self, *args, **kwargs):
		super(FormVariationSelect, self).__init__(*args, **kwargs)
		self.fields['order_number'].queryset = Shipment.objects.filter(payed=True,reconcile=False)
		


class FormVariationLoad(forms.ModelForm):

	class Meta:
		model = PaymentVariation
		exclude = ['payment_number']




class FormShipmentSelect(forms.ModelForm):

	class Meta:
		model = ShipmentPicture
		fields = ['order_number']

	def __init__(self, *args, **kwargs):
		super(FormShipmentSelect, self).__init__(*args, **kwargs)
		self.fields['order_number'].queryset = Shipment.objects.filter(payed=False)



class FormShipmentPicture(forms.ModelForm):

	class Meta:
		model = ShipmentPicture
		exclude = ['order_number','date']

	