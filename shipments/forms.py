from django import forms
from .models import State, ShipmentType, Cost, PriceHistory, Shipment, ShipmentCost

class FormShipment(forms.ModelForm):
    
    class Meta:
        model = Shipment
        exclude = ['start_miles','end_miles', 'delivery_date', 'cost', 'payed']


class FormShipmentCost(forms.ModelForm):
    
    class Meta:
        model = ShipmentCost
        fields = '__all__'

    def __init__(self, user=None, **kwargs):
        super(FormShipmentCost, self).__init__(**kwargs)
        self.fields['order_number'].queryset = Shipment.objects.filter(payed=False,driver=user)
        