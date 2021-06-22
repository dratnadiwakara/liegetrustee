from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator


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
    trust_name = models.CharField(default="",max_length=200,blank=True)
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
    investor_schedule_file = models.FileField(blank=True) 
    investments_file = models.FileField(blank=True) 
    trust_certificates = models.FileField(blank=True) 


    def __str__(self):
        return self.temp_name



class Investor(models.Model):
    securitization = models.ForeignKey(Securitization, on_delete=PROTECT)
    investor_id_no = models.IntegerField()
    investor_name = models.CharField(max_length=200)
    investor_address = models.CharField(max_length=300)
    investor_nic = models.CharField(max_length=20,blank=True)
    investor_account_no = models.CharField(max_length=50)
    investor_account_branch = models.CharField(max_length=100)
    investor_account_bank = models.CharField(max_length=50)
    investor_email = models.EmailField()
    investor_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.investor_name


class Investment(models.Model):
    securitization = models.ForeignKey(Securitization, on_delete=PROTECT)
    investor = models.ForeignKey(Investor, on_delete=PROTECT)
    investment_date = models.DateField()
    maturity_date = models.DateField()
    investment_amount = models.FloatField(validators=[MinValueValidator(0)])
    interest_rate_type = models.PositiveSmallIntegerField( choices=((1,"Fixed"),(2,"AWPLR+")))
    fixed_interest_rate = models.FloatField(validators=[MinValueValidator(0)],blank=True,null=True)
    variable_rate_spread = models.FloatField(blank=True,null=True)
    variable_rate_reset_freq = models.PositiveSmallIntegerField(blank=True,null=True)
    variable_rate_floor = models.FloatField(blank=True,null=True)
    variable_rate_cap = models.FloatField(blank=True,null=True)
    funds_received = models.BooleanField(default=False)
    maturity_proceeds_transfered = models.BooleanField(default=False)
    withheld_tax = models.FloatField(default=0,blank=True)

class Transfer(models.Model):
    securitization = models.ForeignKey(Securitization, on_delete=PROTECT)
    investor = models.ForeignKey(Investor, on_delete=PROTECT,null=True)
    borrower = models.ForeignKey(Borrower, on_delete=PROTECT,null=True)
    amount = models.FloatField()
    transfer_date = models.DateField()
    transfer_complete = models.BooleanField(default=False)


