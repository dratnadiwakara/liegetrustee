from .models import Investor,Investment,Transfer
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
#from django.utils.crypto import get_random_string
import pandas as pd
import django_tables2 as tables
import os
import datetime
# Create your views here.

def index(response):
    return HttpResponse("test")


class InvestorTable(tables.Table):
    class Meta:
        model = Investor 
        exclude=('id','securitization')

class InvestmentTable(tables.Table):
    class Meta:
        model = Investment 
        exclude=('id','securitization')

class TransferTable(tables.Table):
    class Meta:
        model = Transfer 
        exclude=('id','securitization')

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
            #### better method to check if the file exists
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
                "trustee_approved":sec.trustee_approved,
                "investor_set":InvestorTable(sec.investor_set.all()),
                "investment_set":InvestmentTable(sec.investment_set.all()),
                "investor_count":sec.investor_set.all().count(),
                "investment_count":sec.investment_set.all().count(),
                "transfer_set":sec.transfer_set.all().order_by('transfer_date')}

    #print(sec.investor_set.all().count())

    if request.method=="POST" and request.POST['formtype']=="addinvestors":
        if request.FILES.get('investor_file', False)!=False:
            #### Validate if the file is correct format
            sec.investor_schedule_file =request.FILES['investor_file']
            sec.investor_schedule_file.name = "investor_schedule_file_"+str(sec.id)+"."+str(sec.investor_schedule_file).split(".")[1].lower()    
            sec.save()
            investor_table = pd.read_csv(sec.investor_schedule_file)
            #### Convert this to a django-table2
            #investor_table_html = InvestorTable(investor_table.to_dict(orient='list'))
            investor_table_html = investor_table.to_html()
            context["investor_table_html"] = investor_table_html

    if request.method=="POST" and request.POST['formtype']=="confirm_investors":
        investor_table = pd.read_csv(sec.investor_schedule_file)
        lst = list(investor_table)
        investor_table[lst] = investor_table[lst].astype(str)
        for index, row in investor_table.iterrows():
            inv = Investor(securitization=sec,investor_id_no=row['investor_id_no'],investor_name=row['investor_name'],
                            investor_address=row['investor_address'],investor_nic=row['investor_nic'],investor_account_no=row['investor_account_no'],
                            investor_account_branch=row['investor_account_branch'],investor_account_bank=row['investor_account_bank'],
                            investor_email=row['investor_email'],investor_phone=row['investor_phone'])
            inv.save()
    
    if request.method=="POST" and request.POST['formtype']=="addinvestments":
        if request.FILES.get('investments_file', False)!=False:
            #### Validate if the file is correct format
            #### cross check maturity amount if interest rate type = 1
            #### cross check days_to_maturity
            sec.investments_file =request.FILES['investments_file']
            sec.investments_file.name = "investments_file_"+str(sec.id)+"."+str(sec.investor_schedule_file).split(".")[1].lower()    
            sec.save()
            print(sec.investments_file.name)
            investments_table = pd.read_csv(sec.investments_file)
            #### Convert this to a django-table2
            #investor_table_html = InvestorTable(investor_table.to_dict(orient='list'))
            investments_table_html = investments_table.to_html()
            context["investments_table_html"] = investments_table_html
        
    if request.method=="POST" and request.POST['formtype']=="confirm_investments":
        investment_table = pd.read_csv(sec.investments_file)
        investment_table = investment_table.rename(columns={'investment_date_year':'year','investment_date_month':'month','investment_date_date':'day'})
        investment_table['investment_date'] = pd.to_datetime(investment_table[['year','month','day']])
        investment_table = investment_table.drop(['year','month','day'], axis = 1)
        investment_table = investment_table.rename(columns={'maturity_date_year':'year','maturity_date_month':'month','maturity_date_date':'day'})
        investment_table['maturity_date'] = pd.to_datetime(investment_table[['year','month','day']])
        
        investor_cashflows = investment_table.groupby(['investor_id_no','investment_date'],as_index=False)['investment_amount'].sum() 
        for index, row in investor_cashflows.iterrows():
            investor = sec.investor_set.get(investor_id_no=row['investor_id_no']) 
            trans = Transfer(securitization=sec,
                             investor=investor,
                             amount=row['investment_amount'],
                             transfer_date = row['investment_date'])
            trans.save()

        temp = investor_cashflows.groupby(['investment_date'],as_index=False)['investment_amount'].sum() 
        temp['investment_amount'] = -1*temp['investment_amount']
        temp = temp.rename(columns={'investment_date':'maturity_date','investment_amount':'maturity_value'})
        borrower_cashflows = investment_table.groupby(['maturity_date'],as_index=False)['maturity_value'].sum() #### use the maturity amount calculated, not the one uploaded
        borrower_cashflows = borrower_cashflows.append(temp,ignore_index=True)

        for index, row in borrower_cashflows.iterrows():
            trans = Transfer(securitization=sec,
                             borrower=sec.borrower,
                             amount=row['maturity_value'],
                             transfer_date = row['maturity_date'])
            trans.save()

        for index, row in investment_table.iterrows():
            investor = sec.investor_set.get(investor_id_no=row['investor_id_no']) 

            trans = Transfer(securitization=sec,
                             investor=investor,
                             amount= -1*row['maturity_value'],
                             transfer_date = row['maturity_date'])
            trans.save()

            if row['interest_rate_type']==1:
                inv = Investment(securitization=sec,
                                investor=investor,
                                investment_date = row['investment_date'],
                                maturity_date = row['maturity_date'],
                                investment_amount = row['investment_amount'],
                                interest_rate_type = row['interest_rate_type'],
                                fixed_interest_rate = row['fixed_interest_rate'],
                                )
            if row['interest_rate_type']==2:
                inv = Investment(securitization=sec,
                                investor=investor,
                                investment_date = row['investment_date'],
                                maturity_date = row['maturity_date'],                                investment_amount = row['investment_amount'],
                                interest_rate_type = row['interest_rate_type'],
                                variable_rate_spread = row['variable_rate_spread'],
                                variable_rate_reset_freq = row['variable_rate_reset_freq'],
                                variable_rate_floor = row['variable_rate_floor'],
                                variable_rate_cap = row['variable_rate_cap'],
                                )
                        
            inv.save()
    return render(request,"trusteeapp/update_securitization_arranger.html",context)