from django import forms
from django.db.models import fields
from django.forms import widgets
from compound.models import *
from custodian.models import *

class UnitTrustHoldingForm(forms.ModelForm):
    class Meta:
        model = UnitTrustHolding
        fields = ('unit_trust_investor','unit_trust','investment_objective','time_horizon','investment_frequency','investment_amount','nick_name')
        widgets = {'unit_trust_investor':forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(UnitTrustHoldingForm, self).__init__(*args, **kwargs)
        self.fields['unit_trust'].queryset = CustodyClient.objects.filter(client_type='unittrust') #### only liege unit trust ids



class TransferForm(forms.Form):
    holding = forms.ModelChoiceField(queryset=None)

    def __init__(self,invid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['holding'].queryset = UnitTrustHolding.objects.filter(unit_trust_investor=UnitTrustInvestor.objects.get(id=invid))
