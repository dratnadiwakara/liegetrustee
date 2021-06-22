from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.utils.crypto import get_random_string

# Create your models here.
class Borrower(models.Model):
    borrower_name = models.CharField(max_length=200)
    borrower_address = models.CharField(max_length=300)
    borrower_contact_name = models.CharField(max_length=200)
    borrower_contact_number = models.IntegerField()

    def __str__(self):
        return self.borrower_name



class Securitization(models.Model):
    temp_name = models.CharField(max_length=200)
    borrower = models.ForeignKey(Borrower, on_delete=PROTECT)
    arranger_name  = models.CharField(max_length=200) # change this to ForeignKey later
    amount_raised = models.IntegerField()
    expected_sign_date = models.CharField(max_length=200,blank=True) 
    td_firstdraft = models.FileField()
    trust_name = models.CharField(default="",max_length=200)
    trust_bank_account_no = models.CharField(default="",max_length=200,blank=True)
    trust_bank_account_branch = models.CharField(default="",max_length=200,blank=True)
    trust_bank_account_bank = models.CharField(default="",max_length=200,blank=True)
    lawyer_name = models.CharField(max_length=200)
    auditor_name = models.CharField(max_length=200)
    trustee_approved = models.BooleanField(default=False)
    deal_signed = models.BooleanField(default=False)
    cashflow_checked = models.BooleanField(default=False)
    deal_signed_date = models.DateField(blank=True,null=True)
    td_completedraft = models.FileField(blank=True) 
    td_completesigned = models.FileField(blank=True)
    board_resolution = models.FileField(blank=True) 
    information_memo = models.FileField(blank=True) 
    audit_report = models.FileField(blank=True) 


    def __str__(self):
        return self.temp_name