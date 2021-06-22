from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
from django.utils.crypto import get_random_string
import pandas as pd
from django_tables2.tables import Table
import os

# Create your views here.

def index(response):
    return HttpResponse("test")



def create_borrower_view(request):
    form = borrower_form(request.POST or None)

    if form.is_valid():
        form.save()
    
    return render(request,"trusteeapp/create_borrower.html",{"form":form})

# arranger
def create_securitization_view(request):
    if request.method=="POST":
        form = SecuritizationForm(request.POST,request.FILES)
        if form.is_valid():
           form.save()
           return redirect("/create_securitization")
    else:
        form = SecuritizationForm()
    return render(request,"trusteeapp/create_securitization.html",{"form":form})

# trustee
def update_securitization_trustee_view(request,id):
    sec = Securitization.objects.get(id=id)
    form = update_securitization_trustee_form(instance=sec)

    if request.method=="POST" and request.POST['formtype']=="update":
        form = update_securitization_trustee_form(request.POST,instance=sec)
        
        if form.is_valid():
            form.save()
            return redirect("/update_securitization_trustee/"+str(id)+"/")
    
    context = {"form":form,"temp_name":sec.temp_name,
                "borrower_name":sec.borrower.borrower_name,
                "td_firstdraft":sec.td_firstdraft.name,
                "audit_report":sec.audit_report.name,
                "amount_raised":sec.amount_raised,
                "arranger_name":sec.arranger_name,
                "expected_sign_date":sec.expected_sign_date}
    return render(request,"trusteeapp/update_securitization_trustee.html",context)


# trustee
def update_securitization_arranger_view(request,id):
    sec = Securitization.objects.get(id=id)
    form = update_securitization_arranger_form(instance=sec)

    #print(request.POST['formtype'])

    if request.method=="POST" and request.POST['formtype']=="update":
        form = update_securitization_arranger_form(request.POST,request.FILES,instance=sec)
        print(request.POST['formtype'])
        if form.is_valid():
            sec = form.save(commit=False)
            if(sec.td_firstdraft.name != ""):
                sec.td_firstdraft.name = "td_firstdraft_"+str(sec.id)+"."+str(sec.td_firstdraft).split(".")[1].lower()    
            if(sec.td_completedraft.name != ""):
                sec.td_completedraft.name = "td_completedraft_"+str(sec.id)+"."+str(sec.td_completedraft).split(".")[1].lower()    
            if(sec.board_resolution.name != ""):
                sec.board_resolution.name = "board_resolution_"+str(sec.id)+"."+str(sec.board_resolution).split(".")[1].lower() 
            if(sec.information_memo.name != ""):
                sec.information_memo.name = "information_memo_"+str(sec.id)+"."+str(sec.information_memo).split(".")[1].lower()    
            if(sec.audit_report.name != ""):
                sec.audit_report.name = "audit_report_"+str(sec.id)+"."+str(sec.audit_report).split(".")[1].lower()    
            if(sec.td_completesigned.name != ""):
                sec.td_completesigned.name = "td_completesigned_"+str(sec.id)+"."+str(sec.td_completesigned).split(".")[1].lower()    
            sec.save()
            return redirect("/update_securitization_arranger/"+str(id)+"/")
    
    context = {"form":form,"temp_name":sec.temp_name,
                "borrower_name":sec.borrower.borrower_name,
                "trust_name":sec.trust_name,
                "trust_bank_account_no":sec.trust_bank_account_no,
                "trust_bank_account_branch":sec.trust_bank_account_branch,
                "trust_bank_account_bank":sec.trust_bank_account_bank,
                "cashflow_checked":sec.cashflow_checked,
                "trustee_approved":sec.trustee_approved}


    if request.method=="POST" and request.POST['formtype']=="addinvestors":
        investorfile = request.FILES['investor_file']
        investor_table = pd.read_csv(investorfile)
        investor_table_html = investor_table.to_html()
        context["investor_table_html"] = investor_table_html

    return render(request,"trusteeapp/update_securitization_arranger.html",context)