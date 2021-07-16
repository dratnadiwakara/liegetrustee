# exec(open('setupdb/createfunds.py').read()) 

from custodian.models import *
from compound.models import *
from datetime import date, timedelta
import datetime
import pandas as pd
import numpy as np

utinv = UnitTrustInvestor(
    firstname = "UT Inve FN",
    lastname =  "UT Inve LN",
    date_of_birth = "1990-01-01",
    address1 = "address 1",
    phone_number = 425345345,
    bank_account_number  = 5023,
    bank_name = "COMB",
    branch_name = "Nawala",
    nic_number = "907854353V")

utinv.save()

cc = CustodyClient(
    client_name = "Test Margin Client",
    client_address = "Test MC Address",
    client_email = "test@test.com",
    client_phone = "23494304",
    client_type = 'custodian',
    client_birthday = '1982-01-01',
    cds_no_cse = '11130-LC-00',
    cds_no_cbsl = '11130-CB-00',
    margin_interest_rate_spread = 0.25,
    current_account_number = 1000,
    loan_account_number = 1001,
)

cc.save()

cc = CustodyClient(
    client_name = "Liege PF1",
    client_address = "Test MC Address",
    client_email = "test@test.com",
    client_phone = "23494304",
    client_type = 'unittrust',
    client_birthday = '1982-01-01',
    cds_no_cse = '11131-LC-00',
    cds_no_cbsl = '11131-CB-00',
    margin_interest_rate_spread = 0.25,
    current_account_number = 2000,
    loan_account_number = 2001,
    unit_trust_name = "Liege PF1",
    unit_trust_description = "Liege PF1",
    unit_bid_price = 10,
    unit_ask_price = 10,
    number_of_units = 0,
)

cc.save()

cc = CustodyClient(
    client_name = "Liege PF2",
    client_address = "Test MC Address",
    client_email = "test@test.com",
    client_phone = "23494304",
    client_type = 'unittrust',
    client_birthday = '1982-01-01',
    cds_no_cse = '11132-LC-00',
    cds_no_cbsl = '11132-CB-00',
    margin_interest_rate_spread = 0.25,
    current_account_number = 3000,
    loan_account_number = 3001,
    unit_trust_name = "Liege PF2",
    unit_trust_description = "Liege PF2",
    unit_bid_price = 10,
    unit_ask_price = 10,
    number_of_units = 0,
)

cc.save()


cc = CustodyClient(
    client_name = "Liege PF3",
    client_address = "Test MC Address",
    client_email = "test@test.com",
    client_phone = "23494304",
    client_type = 'unittrust',
    client_birthday = '1982-01-01',
    cds_no_cse = '11133-LC-00',
    cds_no_cbsl = '11133-CB-00',
    margin_interest_rate_spread = 0.25,
    current_account_number = 4000,
    loan_account_number = 4001,
    unit_trust_name = "Liege PF3",
    unit_trust_description = "Liege PF3",
    unit_bid_price = 10,
    unit_ask_price = 10,
    number_of_units = 0,
)

cc.save()


cb = ClientBalance(
    client = CustodyClient.objects.filter(cds_no_cse='11130-LC-00')[0],
    value_date = date.today() - timedelta(days=1),
    pf_value = 0,
    margin_value = 0,
    margin_balance = 0,
    pf_cost = 0,
    unit_bid_price = 0,
    unit_ask_price = 0,
    number_of_units = 0)
cb.save()


cb = ClientBalance(
    client = CustodyClient.objects.filter(cds_no_cse='11131-LC-00')[0],
    value_date = date.today() - timedelta(days=1),
    pf_value = 0,
    margin_value = 0,
    margin_balance = 0,
    pf_cost = 0,
    unit_bid_price = 0,
    unit_ask_price = 0,
    number_of_units = 0)
cb.save()

cb = ClientBalance(
    client = CustodyClient.objects.filter(cds_no_cse='11132-LC-00')[0],
    value_date = date.today() - timedelta(days=1),
    pf_value = 0,
    margin_value = 0,
    margin_balance = 0,
    pf_cost = 0,
    unit_bid_price = 0,
    unit_ask_price = 0,
    number_of_units = 0)
cb.save()

cb = ClientBalance(
    client = CustodyClient.objects.filter(cds_no_cse='11133-LC-00')[0],
    value_date = date.today() - timedelta(days=1),
    pf_value = 0,
    margin_value = 0,
    margin_balance = 0,
    pf_cost = 0,
    unit_bid_price = 0,
    unit_ask_price = 0,
    number_of_units = 0)
cb.save()

cb = ClientBalance.objects.all()
for c in cb:
     c.value_date = c.value_date-timedelta(days=1)
     c.save()
'''
h = UnitTrustHoldingHistory.objects.all()
for i in h:
    i.value_date = i.value_date - timedelta(days=1)
    i.save()
'''
ma = MarginAccount(
    client = CustodyClient.objects.filter(cds_no_cse='11130-LC-00')[0],
    trade_date = date.today() - timedelta(days=1),
    amount = 0)
ma.save()

ma = MarginAccount(
    client = CustodyClient.objects.filter(cds_no_cse='11131-LC-00')[0],
    trade_date = date.today() - timedelta(days=1),
    amount = 0)
ma.save()

ma = MarginAccount(
    client = CustodyClient.objects.filter(cds_no_cse='11132-LC-00')[0],
    trade_date = date.today() - timedelta(days=1),
    amount = 0)
ma.save()

ma = MarginAccount(
    client = CustodyClient.objects.filter(cds_no_cse='11133-LC-00')[0],
    trade_date = date.today() - timedelta(days=1),
    amount = 0)
ma.save()





ca = CurrentAccount(
    client = CustodyClient.objects.filter(cds_no_cse='11130-LC-00')[0],
    transaction_date = date.today() - timedelta(days=1),
    amount = 0,
    narration="")
ca.save()

ca = CurrentAccount(
    client = CustodyClient.objects.filter(cds_no_cse='11131-LC-00')[0],
    transaction_date = date.today() - timedelta(days=1),
    amount = 0,
    narration="")
ca.save()

ca = CurrentAccount(
    client = CustodyClient.objects.filter(cds_no_cse='11132-LC-00')[0],
    transaction_date = date.today() - timedelta(days=1),
    amount = 0,
    narration="")
ca.save()

ca = CurrentAccount(
    client = CustodyClient.objects.filter(cds_no_cse='11133-LC-00')[0],
    transaction_date = date.today() - timedelta(days=1),
    amount = 0,
    narration="")
ca.save()


sb = StockBroker(
    broker_name="SMS",
    broker_code="SMB Capital"
)

sb.save()