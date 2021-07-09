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
from custodian.forms import *
from django.db.models import Sum
# Create your views here.


def index(response):
    return HttpResponse("test custodian")

def create_client(request):
    if request.method=="POST":
        form = ClientForm(request.POST)
        if form.is_valid():
           client = form.save()
           return redirect("/custodian/createholding/"+str(client.id)+"/")
    else:
        form = ClientForm()
    return render(request,"custodian/create_client.html",{"form":form})


def create_holdings(request,id):
    #### pass client name, id, portfolio list, and client to context, in addition to the form
    client = CustodyClient.objects.get(id=id)
    holdings = EquityHolding.objects.filter(client=client)
    if request.method=="POST":
        form = HoldingForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect("/custodian/createholding/"+str(id)+"/")
    else:
        form = HoldingForm(initial={'client': client})
    return render(request,"custodian/create_holding.html",{"form":form,"client":client,"equitypf":holdings})



def transhistory(request):
    context={"transhistory": MarginAccount.objects.filter(client=Client.objects.filter(client_id="11130-LC-00")[0]).order_by('-trade_date')}
    return render(request,"custodian/transhistory.html",context)


def pfsummary(request):
    client = Client.objects.filter(client_id="11130-LC-00")[0]
    #### replace this with logged in client
    holdings = EquityHolding.objects.filter(client=client)
 
    context =   {"equitypf":holdings,
                "client":client,
            }

    cb = pd.DataFrame(list(ClientBalance.objects.filter(client=client).values()))
    cb['value_date'] = pd.to_datetime(cb['value_date']) 
    cb['value_date'] = cb['value_date'].dt.strftime('%y-%m-%d')
    cb['margin_balance'] = cb['margin_balance']*(-1)
    context["dates"]=cb['value_date'].to_list()
    context["pf_value"]=cb['pf_value'].to_list()
    context["margin_value"]=cb['margin_value'].to_list()
    context["margin_balance"]=cb['margin_balance'].to_list()
    context["pf_cost"]=cb['pf_cost'].to_list()
    
    return render(request,"custodian/viewpf.html",context)
    

def uploaddocs(request):
    form = UploadDocument()
    context = {"form":form}


    if request.method=="POST" and request.POST['doctype']=="currentaccountbal":
        if request.FILES.get('datafile', False)!=False:
            curacc = pd.read_csv(request.FILES['datafile'])
            print(curacc)
            curacc['dateofbalance']=pd.to_datetime(curacc['dateofbalance'])
            for index,row in curacc.iterrows():
                #### check if dateofbalance is today.
                cl = CustodyClient.objects.filter(current_account_number=row['accountnumber'])[0]
                print(cl)
                print(row['dateofbalance'])
                print(row['balanceamount'])
                #### show if cl doesnot exist
                ma = MarginAccount(client=cl,current_account_sweep=True,trade_date=row['dateofbalance'],amount=row['balanceamount'])
                ma.save()

    if request.method=="POST" and request.POST['doctype']=="reconmargin":
        #### receive the margin balances from corebanking
        #### compare margin balance from corebanking to margin balance
        #### report # matching, # not matching, show list of not matching
        pass

    if request.method=="POST" and request.POST['doctype']=="reconcds":
        #### receive the cds transfer document
        #### compare 
        #### report # matching, # not matching, show list of not matching
        pass

    if request.method=="POST" and request.POST['doctype']=="clientbalance":
        #### check if equityprice, cdsimport, and currentaccount import are all complete for the day
        #### warnings if all the above files have not been updated
        clients = CustodyClient.objects.all()
        for cl in clients:
            cl.margin_account_balance = MarginAccount.objects.filter(client=cl).aggregate(Sum('amount'))['amount__sum']
            if(cl.margin_account_balance==None):
                cl.margin_account_balance=0
            print(cl)
            pf_value = 0
            margin_value = 0
            pf_cost = 0
            holdings = EquityHolding.objects.filter(client=cl)
            for h in holdings:
                pf_value = pf_value+h.marketvalue
                margin_value = margin_value+h.marginvalue
                pf_cost = pf_cost+h.cost_basis*h.quantity
            cb = ClientBalance(client=cl,pf_value=pf_value,margin_value=margin_value,margin_balance=cl.margin_account_balance,pf_cost=pf_cost)
            cb.save()
            cl.portfolio_value = pf_value
            cl.maximum_margin = margin_value
            cl.save()
            #### set payable amount
            #### set receivable amount
            #### add margin interest as an entry to MarginAccount

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
            #### Show a count of number of trades created, number and list of failed records
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
                    if not EquityTrade.objects.filter(trx_contract=tr.trx_contract).exists():
                        tr.save()
                    #else:
                    #    print("trade already exists") #### better way  to makesure there are no trade duplicates?
            except Exception as e:
                print('Error While Importing Data: ',e)

    return render(request,"custodian/uploaddocuments.html",context)
