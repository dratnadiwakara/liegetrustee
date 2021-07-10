from django.db import models
from django.db.models.deletion import PROTECT

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

class FundManager(models.Model):
    fund_manager_name = models.CharField(max_length=200)
    def __str__(self):
        return self.fund_manager_name

class UnitTrust(models.Model):
    fund_manager = models.ForeignKey(FundManager,on_delete=PROTECT)
    portfolio_name = models.CharField(max_length=200)
    portfolio_description = models.TextField()
    unit_bid_price = models.FloatField()
    unit_ask_price = models.FloatField()
    number_of_units = models.FloatField()

    def __str__(self):
        return self.portfolio_name

class UnitTrustHistory(models.Model):
    unit_trust = models.ForeignKey(UnitTrust,on_delete=PROTECT)
    unit_bid_price = models.FloatField()
    unit_ask_price = models.FloatField()
    number_of_units = models.FloatField()
    history_date = models.DateField(auto_now_add=True, blank=True)

class UnitTrustHolding(models.Model):
    unit_trust_investor = models.ForeignKey(UnitTrustInvestor,on_delete=PROTECT)
    unit_trust = models.ForeignKey(UnitTrust,on_delete=PROTECT)
    number_of_units = models.IntegerField()
    cost_basis = models.FloatField()
    nick_name = models.CharField(max_length=100)


class Transaction(models.Model):
    TRANS_TYPE = [('purchase','Unit purchase'),('redemption','Unit redemption'),
    ('transfer','Fund transfer to investor')]
    unit_trust_investor = models.ForeignKey(UnitTrustInvestor,on_delete=PROTECT)
    unit_trust_holding = models.ForeignKey(UnitTrustHolding,on_delete=PROTECT)
    transaction_type = models.CharField(choices=TRANS_TYPE)
    purchase_amount = models.FloatField(null=True,blank=True)
    purchase_price = models.FloatField(null=True)
    number_of_units_purchased = models.FloatField(null=True)
    redemption_amount = models.FloatField(null=True)
    redemption_price =  models.FloatField(null=True)
    number_of_units_redeemed = models.FloatField(null=True)
    transaction_processed = models.BooleanField(default=False)


