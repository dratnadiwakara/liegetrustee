from django.shortcuts import render,redirect
from compound.models import *
from compound.forms import *


def index(request,id):
    investor = UnitTrustInvestor.objects.get(id=id)
    holdings = UnitTrustHolding.objects.filter(unit_trust_investor=investor)
    context =   {"investor":investor,
                "unittrustholdings":holdings,
            }
    return render(request,"compound/compound_home.html",context)


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