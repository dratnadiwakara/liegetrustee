from django import forms
from django.db.models import fields
from django.forms import widgets
from custodian.models import *


class UploadDocument(forms.Form):
    datafile = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))



class ClientForm(forms.ModelForm):
    class Meta:
        model = CustodyClient
        fields = ('client_name','client_address','client_email','client_phone',
        'client_type','client_birthday','margin_interest_rate_spread','current_account_number',
        'loan_account_number','shariah_compliant','risk_appetite','target_returns',
        'cds_no_cse','cds_no_cbsl')
        #### date pricker for birthday

class HoldingForm(forms.ModelForm):
    class Meta:
        model = EquityHolding
        fields = ('client','stock','quantity','cost_basis','broker')
        widgets = {'client':forms.HiddenInput()}
        #### client should be set to the added client by default. This form is typically shown after adding a new client. 
        