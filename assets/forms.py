from django import forms
from .models import *
from recpoint.users.models import *
from shipments.models import *


class FormDriverPayment(forms.ModelForm):

	class Meta:
		model = Shipment
		fields = ['driver']

	def __init__(self,  *args, **kwargs):
		super(FormDriverPayment, self).__init__( *args, **kwargs)
		self.fields['driver'].queryset = User.objects.filter(groups__name='Driver')