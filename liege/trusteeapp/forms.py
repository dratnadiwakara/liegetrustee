from django import forms
from django.db.models import fields
from .models import Borrower,Securitization




class borrower_form(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = '__all__'


class SecuritizationForm(forms.ModelForm):
    class Meta:
        model = Securitization
        fields = ('temp_name','borrower','lawyer_name','auditor_name'
       ,"arranger_name","amount_raised","expected_sign_date")
        # add date picker for expected_sign_date

class update_securitization_trustee_form(forms.ModelForm):
    class Meta:
        model = Securitization
        fields = ('trust_name','trust_bank_account_no','trust_bank_account_branch',
        'trust_bank_account_bank',"trustee_approved","cashflow_checked","deal_signed","deal_signed_date")
        # add date picker for deal_signed_date



class update_securitization_arranger_form(forms.ModelForm):
    class Meta:
        model = Securitization
        fields = ('td_firstdraft','amount_raised','lawyer_name','auditor_name','td_completedraft','td_completesigned','board_resolution','audit_report','information_memo')
        # add date picker for deal_signed_date  ,
