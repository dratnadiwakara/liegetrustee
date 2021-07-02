from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date,timedelta

"""
EOD==============
Update equity prices
Upload dividend announcements
Upload splits
Upload scrip dividends
Upload CDS transaction records
    Update trades
    Calculate margin
    Calculate payable amount
    Calculate receivable amount
    Calculate CDS transfer amount
Download CDS settlement balance instructions
Update current account balances
    Sweep current account balance to margin account 
Update ClientHistory


History tables for All Uploads, date,time, file, username
"""

class Client(models.Model):
    
    CLIENT_TYPES = [('custodian','Custodian Client'),
                    ('margin','Margin Client'),
                    ('unittrust','Unit Trust'),]

    client_name = models.CharField(max_length=200)
    client_address = models.CharField(max_length=200)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20)
    client_type = models.CharField(max_length=20,choices=CLIENT_TYPES)
    portfolio_value = models.FloatField(default=0,null=True)
    portfolio_value_date = models.DateField(null=True)
    margin_account_balance = models.FloatField(default=0)
    margin_account_balance_date = models.DateField()
    maximum_margin = models.FloatField()
    maximum_margin_date = models.DateField()
    payable_amount = models.FloatField()
    payable_amount_date = models.DateField()
    receivable_amount = models.FloatField()
    receivable_amount_date = models.DateField()
    client_id = models.CharField(max_length=200)



class CustodyClientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(client_type='custodian')

class CustodyClient(Client):
    objects = CustodyClientManager()
    class Meta:
        proxy = True

class ListedEquity(models.Model):
    ticker = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    current_price = models.FloatField()
    current_price_date = models.DateField()
    in_sl20 = models.BooleanField()
    margin_pct = models.FloatField(default=0.50)

class DividendAnnouncements(models.Model):
    equity = models.ForeignKey(ListedEquity,on_delete=CASCADE)
    dividend_amount = models.FloatField()
    ex_date = models.DateField()
    updated_date = models.DateTimeField(auto_now_add=True, blank=True)

class StockBroker(models.Model):
    broker_name=models.CharField(max_length=200)
    broker_code=models.CharField(max_length=5,default="AAA")

class EquityTrade(models.Model):
    #tr = EquityTrade(client=CustodyClient.objects.get(id=1),stock=ListedEquity.objects.get(id=1),trade_price=200,trade_quantity=2000,trade_direction='buy',broker=StockBroker.objects.get(id=1),trade_date=datetime.date.today())
    DIRECTION = [('buy','Buy'),('sell','Sell')]
    client = models.ForeignKey(Client,on_delete=PROTECT)
    stock = models.ForeignKey(ListedEquity,on_delete=PROTECT)
    trade_price = models.FloatField()
    trade_quantity = models.FloatField()
    trade_date = models.DateField()
    settlement_date = models.DateField()
    trade_direction = models.CharField(max_length=10,choices=DIRECTION)
    broker = models.ForeignKey(StockBroker,on_delete=PROTECT)
    brokerage = models.FloatField(default=0)
    cds_fees = models.FloatField(default=0)
    sec_cess = models.FloatField(default=0)
    btt = models.FloatField(default=0)
    cse_fees = models.FloatField(default=0)
    stamp_duty = models.FloatField(default=0)
    govt_cess = models.FloatField(default=0)
    trx_contract = models.CharField(primary_key=True,max_length=200)

    @property
    def amount(self):
        return self.trade_quantity*self.trade_price
    
    @property
    def fees(self):
        return self.brokerage + self.cds_fees + self.sec_cess+self.btt + self.cse_fees+ self.stamp_duty + self.govt_cess

    @property
    def netamount(self):
        if self.trade_direction=='buy':
            return (self.amount+self.fees)*(-1)
        else:
            return (self.amount-self.fees)


    def save(self, *args,**kwargs):

        fees = self.brokerage + self.cds_fees + self.sec_cess+self.btt + self.cse_fees+ self.stamp_duty + self.govt_cess

        if self.trade_direction=='buy':
            amt = self.trade_price*self.trade_quantity+fees
            amt = amt*(-1)
        elif self.trade_direction=='sell':
            amt = self.trade_price*self.trade_quantity-fees

        pos = self.client.equityholding_set.filter(stock=self.stock).filter(broker=self.broker)
        if(pos.count()==1) :
            pos = pos[0]
            pos.cost_basis = (pos.cost_basis*pos.quantity+self.trade_quantity*self.trade_price)/(pos.quantity+self.trade_quantity)
            pos.quantity = pos.quantity+self.trade_quantity
        else:
            pos = EquityHolding(client=self.client,stock=self.stock,quantity = self.trade_quantity,cost_basis=self.trade_price,broker=self.broker)
        pos.save()

        super(EquityTrade, self).save(*args, **kwargs)

        # MarginAccount entry
        marginacc = MarginAccount(client=self.client,trade=self,trade_date=self.trade_date,settlement_date=self.settlement_date,debit=self.trade_direction=='buy',amount=amt)
        marginacc.save()
        # CDS Account entry
        cdsacc = CDSAccount(client=self.client,trade=self,settlement_date=self.settlement_date,trade_date=self.trade_date,credit=self.trade_direction=='buy',amount=amt)
        cdsacc.save()

        super(EquityTrade, self).save(*args, **kwargs)


class EquityHolding(models.Model):
    client = models.ForeignKey(Client,on_delete=PROTECT)
    stock = models.ForeignKey(ListedEquity,on_delete=PROTECT)
    quantity = models.FloatField()
    cost_basis = models.FloatField()
    broker = models.ForeignKey(StockBroker,on_delete=PROTECT,null=True)
    last_updated= models.DateTimeField(auto_now_add=True, blank=True)

    @property
    def marketvalue(self):
        return self.quantity*self.stock.current_price

    @property
    def gainloss(self):
        return self.quantity*(self.stock.current_price-self.cost_basis)

    @property
    def marginvalue(self):
        return self.quantity*self.stock.current_price*self.stock.margin_pct


class MarginAccount(models.Model):
    client = models.ForeignKey(Client,on_delete=PROTECT)
    current_account_sweep = models.BooleanField(default=False)
    trade = models.ForeignKey(EquityTrade,on_delete=CASCADE)
    trade_date = models.DateField()
    settlement_date = models.DateField()
    debit = models.BooleanField()
    amount = models.FloatField()

class CDSAccount(models.Model):
    client = models.ForeignKey(Client,on_delete=PROTECT)
    balance_transfer_to_CDS = models.BooleanField(default=False)
    trade = models.ForeignKey(EquityTrade,on_delete=CASCADE)
    trade_date = models.DateField()
    settlement_date = models.DateField()
    credit = models.BooleanField()
    amount = models.FloatField()

class ClientHistory(models.Model):
    client = models.ForeignKey(Client,on_delete=PROTECT)
    portfolio_value = models.FloatField()
    margin_balance = models.FloatField()

class Uploads(models.Model):
    UPLOAD_TYPES = [('equityprices','Equity Price List'),('cdstrades','CDS Trade List')]
    upload_date = models.DateField(auto_now_add=True, blank=True)
    uploaded_file = models.FileField()
    #### change the following to logged in user
    uploaded_by = models.CharField(max_length=200,blank=True,null=True)
    upload_type = models.CharField(max_length=20,choices=UPLOAD_TYPES)
