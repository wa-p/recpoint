from django import forms
from .models import *

class FormShipment(forms.ModelForm):

	class Meta:
		model = Shipment
		exclude = ['driver','end_miles', 'delivery_date', 'cost', 'payed','payed_driver','order_picture','payed_driver_date']

	def __init__(self, *args, **kwargs):
		super(FormShipment, self).__init__(*args, **kwargs)
		self.fields['trailer'].queryset = Vehicle.objects.filter(vehicle_type='Trailer',status='Ok')
		self.fields['truck'].queryset = Vehicle.objects.filter(vehicle_type='Truck',status='Ok')


class FormShipmentCost(forms.ModelForm):
    
	class Meta:
		model = ShipmentCost
		fields = '__all__'

	def __init__(self, user, *args, **kwargs):
		super(FormShipmentCost, self).__init__(*args, **kwargs)
		if User.objects.get(id=user.id).groups.filter(name='Management').exists():
			self.fields['order_number'].queryset = Shipment.objects.filter(payed=False).order_by('-order_date')	
		else:
			self.fields['order_number'].queryset = Shipment.objects.filter(payed=False,driver=user).order_by('-order_date')


class FormLastShipmentCost(forms.ModelForm):
    
	class Meta:
		model = ShipmentCost
		fields = '__all__'

	def __init__(self, user, *args, **kwargs):
		super(FormLastShipmentCost, self).__init__(*args, **kwargs)
		self.fields['expense_type'].initial = ['Gas']
		self.fields['expense_type'].disabled = True
		if User.objects.get(id=user.id).groups.filter(name='Management').exists():
			self.fields['order_number'].queryset = Shipment.objects.filter(last_expense=False,end_miles__gt=0).order_by('-order_date')	
		else:
			self.fields['order_number'].queryset = Shipment.objects.filter(last_expense=False,end_miles__gt=0,driver=user).order_by('-order_date')


class FormPayment(forms.ModelForm):

	class Meta:
		model = Payment
		fields = '__all__'

	def __init__(self,  *args, **kwargs):
		super(FormPayment, self).__init__( *args, **kwargs)
		self.fields['order_number'].queryset = Shipment.objects.filter(payed=False)


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