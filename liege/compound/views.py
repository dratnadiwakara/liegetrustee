from django.shortcuts import render,redirect
from compound.models import *
from compound.forms import *
import pandas as pd


def index(request,id):
    investor = UnitTrustInvestor.objects.get(id=id)
    holdings = UnitTrustHolding.objects.filter(unit_trust_investor=investor)
    context =   {"investor":investor,
                "unittrustholdings":holdings,
            }
    return render(request,"compound/compound_home.html",context)


def holdingview(request,id):
    holding = UnitTrustHolding.objects.get(id=id)
    transactions = Transaction.objects.filter(unit_trust_holding=holding)
    #### replace this with logged in client
    context = {"holding":holding,"transactions":transactions}

    cb = pd.DataFrame(list(UnitTrustHoldingHistory.objects.filter(unit_trust_holding=holding).values()))
    cb['value_date'] = pd.to_datetime(cb['value_date']) 
    cb['value_date'] = cb['value_date'].dt.strftime('%y-%m-%d')
    cb['pf_value'] = cb['unit_price']*cb['number_of_units']
    

    context["dates"]=cb['value_date'].to_list()
    context["number_of_units"]=cb['number_of_units'].to_list()
    context["unit_price"]=cb['unit_price'].to_list()
    context["pf_value"]=cb['pf_value'].to_list()
    
    return render(request,"compound/viewholding.html",context)


def create_unittrust_holdings(request,id):
    #### pass client name, id, portfolio list, and client to context, in addition to the form
    investor = UnitTrustInvestor.objects.get(id=id)
    
    if request.method=="POST":
        form = UnitTrustHoldingForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect("/compound/"+str(id)+"/")
    else:
        form = UnitTrustHoldingForm(initial={'unit_trust_investor': investor})
    return render(request,"compound/create_unittrust_holding.html",{"form":form,"unit_trust_investor":investor})



def transfer_funds(request,id):
    investor = UnitTrustInvestor.objects.get(id=id)

    form = TransferForm(id)
    return render(request,"compound/fundtransfer.html",{"form":form,"unit_trust_investor":investor})