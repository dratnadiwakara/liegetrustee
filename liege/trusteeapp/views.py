from .models import *
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
#from django.utils.crypto import get_random_string
import pandas as pd
import django_tables2 as tables
import os
import datetime
from django.http import JsonResponse
import json

# Create your views here.

def index(response):
    return HttpResponse("test")


# trustee
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
def view_securitizations(request):
    current = Securitization.objects.filter(trustee_approved=False)
    past = Securitization.objects.filter(trustee_approved=True)
    context = {"currentdeals":current,"pastdeals":past}
    return render(request,"trusteeapp/view_securitizations.html",context)

# arranger
def view_securitizations_current_arranger(request):
    current = Securitization.objects.filter(trustee_approved=False)
    context = {"currentdeals":current}
    return render(request,"trusteeapp/view_securitizations_current_arranger.html",context)

# arranger
def view_securitizations_past_arranger(request):
    past = Securitization.objects.filter(trustee_approved=True)
    context = {"pastdeals":past}
    return render(request,"trusteeapp/view_securitizations_past_arranger.html",context)

# trustee
def view_transfers(request):
    current = Transfer.objects.filter(transfer_complete=False)
    past = Transfer.objects.filter(transfer_complete=True)
    context = {"pending":current,"pasttrans":past}
    return render(request,"trusteeapp/view_transfers.html",context)

# trustee
def update_securitization_trustee_view(request,id):
    sec = Securitization.objects.get(id=id)
    form = update_securitization_trustee_form(instance=sec)

    context = {"form":form,
                "securitization":sec,}

    if sec.security_set.all().count() > 0:
        secset = sec.security_set.all()
        secdf = pd.DataFrame(list(secset.values()))
        t = pd.date_range(start=datetime.date.today(),end=max(secdf['last_payment_date']),freq="MS")
        cf = pd.DataFrame(0,index=t,columns=['cashflow'])
        for index, row in secdf.iterrows():
            stdate = datetime.date.today()
            while stdate < row['last_payment_date']:
                stdate = datetime.date(stdate.year + int(stdate.month / 12), ((stdate.month % 12) + 1), 1)
                cf.loc[stdate.strftime("%Y-%m-%d"),'cashflow'] = cf.loc[stdate.strftime("%Y-%m-%d"),'cashflow']+row['monthly_payment']
            
        tf = pd.DataFrame(list(sec.borrower.transfer_set.all().filter(amount__gte=0).values()))
        tf = tf[['amount','transfer_date']]
        tf['transfer_date'] = tf['transfer_date'].apply(lambda datetime: datetime.replace(day=1))
        tf.set_index('transfer_date',inplace=True)
        tf = cf.join(tf,how="outer")
        tf['amountcc']=tf.amount*1.3
        tf['cf_date'] = tf.index.strftime("%y-%m")
        context["payment_dates"] = tf['cf_date'].to_list()
        context["amount"] = tf['amount'].to_list()
        context["amountcc"] = tf['amountcc'].to_list()
        context["cashflow"] = tf['cashflow'].to_list()


    if request.method=="POST" and request.POST['formtype']=="update":
        form = update_securitization_trustee_form(request.POST,instance=sec)
        
        if form.is_valid():
            form.save()
    return render(request,"trusteeapp/update_securitization_trustee.html",context)

# arranger
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

    context = {"form":form,
                "securitization":sec,}

    if sec.security_set.all().count() > 0:
        secset = sec.security_set.all()
        secdf = pd.DataFrame(list(secset.values()))
        t = pd.date_range(start=datetime.date.today(),end=max(secdf['last_payment_date']),freq="MS")
        cf = pd.DataFrame(0,index=t,columns=['cashflow'])
        for index, row in secdf.iterrows():
            stdate = datetime.date.today()
            while stdate < row['last_payment_date']:
                stdate = datetime.date(stdate.year + int(stdate.month / 12), ((stdate.month % 12) + 1), 1)
                cf.loc[stdate.strftime("%Y-%m-%d"),'cashflow'] = cf.loc[stdate.strftime("%Y-%m-%d"),'cashflow']+row['monthly_payment']
            
        tf = pd.DataFrame(list(sec.borrower.transfer_set.all().filter(amount__gte=0).values()))
        tf = tf[['amount','transfer_date']]
        tf['transfer_date'] = tf['transfer_date'].apply(lambda datetime: datetime.replace(day=1))
        tf.set_index('transfer_date',inplace=True)
        tf = cf.join(tf,how="outer")
        tf['amountcc']=tf.amount*1.3
        tf['cf_date'] = tf.index.strftime("%y-%m")
        context["payment_dates"] = tf['cf_date'].to_list()
        context["amount"] = tf['amount'].to_list()
        context["amountcc"] = tf['amountcc'].to_list()
        context["cashflow"] = tf['cashflow'].to_list()

                

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

    if request.method=="POST" and request.POST['formtype']=="addsecurities":
        if request.FILES.get('securities_file', False)!=False:
            #### Validate if the file is correct format
            sec.security_list_file =request.FILES['securities_file']
            sec.security_list_file.name = "securities_file_"+str(sec.id)+"."+str(sec.investor_schedule_file).split(".")[1].lower()    
            sec.save()

            securities_table = pd.read_csv(sec.security_list_file)
            #### Convert this to a django-table2
            #investor_table_html = InvestorTable(investor_table.to_dict(orient='list'))
            securities_table_html = securities_table.to_html()
            context["securities_table_html"] = securities_table_html

    if request.method=="POST" and request.POST['formtype']=="confirm_securities":
        securities_table = pd.read_csv(sec.security_list_file)
        securities_table = securities_table.rename(columns={'last_payment_date_year':'year','last_payment_date_month':'month','last_payment_date_date':'day'})
        securities_table['last_payment_date'] = pd.to_datetime(securities_table[['year','month','day']])
  
        for index, row in securities_table.iterrows():
            #### add other variables as attributes
            scr = Security(securitization=sec,
                            added_date = datetime.date.today(),
                            engine_number = row['engine_number'],
                            chassis_number = row['chassis_number'],
                            monthly_payment = row['monthly_payment'],
                            last_payment_date = row['last_payment_date'],

            )
            scr.save()

    return render(request,"trusteeapp/update_securitization_arranger.html",context)