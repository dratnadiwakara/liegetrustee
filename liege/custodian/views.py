from django.shortcuts import redirect, render
from django.http import HttpResponse
from custodian.forms import *
from custodian.models import *
import pandas as pd
from django.db.models import Sum
import datetime
import csv
import io
import json
import numpy as np
# Create your views here.


def index(response):
    return HttpResponse("test custodian")

def transhistory(request):
    context={"transhistory": MarginAccount.objects.filter(client=Client.objects.filter(client_id="11130-LC-00")[0]).order_by('-trade_date')}
    return render(request,"custodian/transhistory.html",context)


def pfsummary(request):
    client = Client.objects.filter(client_id="11130-LC-00")[0]
    holdings = EquityHolding.objects.filter(client=client)
    pfsummary = {"mktvalue":0,"marginvalue":0,"totalcost":0,"totalgainloss":0}
    for h in holdings:
        pfsummary['mktvalue'] = pfsummary['mktvalue']+h.marketvalue
        pfsummary['marginvalue'] = pfsummary['marginvalue']+h.marginvalue
        pfsummary['totalcost'] = pfsummary['totalcost']+h.cost_basis*h.quantity
        pfsummary['totalgainloss'] = pfsummary['totalgainloss']+h.gainloss

    context =   {"equitypf":holdings,
                 "mktvalue": pfsummary['mktvalue'],
                 "totalcost": pfsummary['totalcost'],
                 "marginvalue": pfsummary['marginvalue'],
                 "totalgainloss": pfsummary['totalgainloss'],
                }
    
    return render(request,"custodian/viewpf.html",context)
    

def uploaddocs(request):
    form = UploadDocument()
    context = {"form":form}


    if request.method=="POST" and request.POST['doctype']=="currentaccountbal":
        if request.FILES.get('datafile', False)!=False:
            #### read currentaccount balance file csv.
            #### move the balance to margin account
            pass

    if request.method=="POST" and request.POST['doctype']=="clientbalance":
        if request.FILES.get('datafile', False)!=False:
            #### set portfolio value
            #### set clients margin account balance
            #### set maximum margin, excess margin
            #### set payable amount
            #### set receivable amount
            #### add data for time series graph
            pass

    if request.method=="POST" and request.POST['doctype']=="equityprices":
        if request.FILES.get('datafile', False)!=False:
            #### keep a record of upload time
            #### upload = Uploads(uploaded_file=request.FILES['datafile'],upload_type='equityprices')
            #### upload.uploaded_file.name="equitydata.csv"
            #### upload.save()
            equityprc = pd.read_csv(request.FILES['datafile'],header=None, dtype={4: str})
            equityprc['security_id'] = equityprc[[2,3,4]].agg('-'.join, axis=1)
            equityprc.rename({9: 'price'}, axis=1, inplace=True)

            for index,row in equityprc.iterrows():
                try:
                    e = ListedEquity.objects.filter(ticker=row['security_id'])[0]
                    e.current_price = row['price']
                    e.save()
                except Exception as e:
                    pass


    if request.method=="POST" and request.POST['doctype']=="cdstrades":
        if request.FILES.get('datafile', False)!=False:
            #### check if the date of the csv column is equal to the current date?
            #### keep a record of upload time
            #### upload = Uploads(uploaded_file=request.FILES['datafile'],upload_type='cdstrades')
            #### upload.uploaded_file.name="cdstrades.csv"
            #### upload.save()
            cdsdata = pd.read_csv(request.FILES['datafile'])
            cdsdata.columns = [c.strip().lower().replace(' ', '_') for c in cdsdata.columns]
            cdsdata['trade_date']=pd.to_datetime(cdsdata['trade_date'])
            cdsdata['settlement_date']=pd.to_datetime(cdsdata['settlement_date'])
            cdsdata['buy_sell1'] = np.where(cdsdata['buy_sell1'].str.strip()=='BOUGHT FROM','buy','sell')

            trades = [
                EquityTrade(
                    client=CustodyClient.objects.filter(client_id=row['client_id'].strip())[0],
                    stock=ListedEquity.objects.filter(ticker=row['security_id'].strip())[0],
                    trade_price=row['price'],
                    trade_quantity=row['qty'],
                    trade_date= row['trade_date'],
                    settlement_date=row['settlement_date'],
                    trade_direction='buy',
                    broker=StockBroker.objects.filter(broker_code=row['broker_code'].strip())[0],
                    brokerage=row['brokerage'],
                    cds_fees=row['cds_fees'],
                    sec_cess=row['sec_cess'],
                    btt=row['btt'],
                    cse_fees=row['cse_fees'],
                    stamp_duty=row['stamp_duty'],
                    govt_cess=row['govt_cess'],
                    trx_contract=row['trx_contract'].strip()
                )  for index,row in cdsdata.iterrows()
            ]
            
            try:
                for tr in trades:
                    tr.save()
                print('imported successfully')
            except Exception as e:
                print('Error While Importing Data: ',e)

    return render(request,"custodian/uploaddocuments.html",context)
