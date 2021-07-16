from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
import custodian.models  as custodian_models

# Create your models here.


# use the user module to implement investor
class UnitTrustInvestor(models.Model):
    firstname = models.CharField(max_length=200)
    lastname =  models.CharField(max_length=200)
    date_of_birth = models.DateField()
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200,null=True,blank=True)
    phone_number = models.PositiveIntegerField()
    bank_account_number  = models.PositiveIntegerField()
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    bank_statement  = models.FileField(null=True)
    nic_number = models.CharField(max_length=20)
    nic_copy_side1 = models.FileField(null=True)
    nic_copy_side2 = models.FileField(null=True)
    headshot = models.FileField(null=True)
    account_open_date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.firstname+" "+self.lastname


class UnitTrustHolding(models.Model):
    INV_FREQ = [('weekly','Every week'),('monthly','Every month'),
    ('quarterly','Every quarter'),('annually',"Every year")]
    unit_trust_investor = models.ForeignKey(UnitTrustInvestor,on_delete=PROTECT)
    unit_trust = models.ForeignKey(custodian_models.CustodyClient,on_delete=PROTECT)
    number_of_units = models.IntegerField(default=0)
    cost_basis = models.FloatField(default=0)
    nick_name = models.CharField(max_length=100)
    investment_objective = models.CharField(max_length=200)
    time_horizon = models.PositiveIntegerField()
    investment_frequency = models.CharField(choices=INV_FREQ,max_length=50)
    investment_amount = models.FloatField()


    def __str__(self):
        return self.nick_name+"-"+str(self.id)
    @property
    def value(self):
        return str(self.unit_trust.unit_bid_price*self.number_of_units)

class UnitTrustHoldingHistory(models.Model):
    unit_trust_holding = models.ForeignKey(UnitTrustHolding,on_delete=CASCADE)
    value_date = models.DateField(auto_now_add=True, blank=True)
    number_of_units = models.IntegerField()
    unit_price = models.FloatField()

class Transaction(models.Model):
    TRANS_TYPE = [('purchase','Unit purchase'),('redemption','Unit redemption'),
    ('transfer','Fund transfer to investor')]
    unit_trust_holding = models.ForeignKey(UnitTrustHolding,on_delete=PROTECT)
    transaction_type = models.CharField(choices=TRANS_TYPE,max_length=50)
    transaction_date = models.DateField(auto_now_add=True, blank=True)
    purchase_amount = models.FloatField(null=True,blank=True)
    purchase_price = models.FloatField(null=True)
    number_of_units_purchased = models.FloatField(null=True)
    redemption_amount = models.FloatField(null=True)
    redemption_price =  models.FloatField(null=True)
    number_of_units_redeemed = models.FloatField(null=True)
    transaction_processed = models.BooleanField(default=False)