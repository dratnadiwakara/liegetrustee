# exec(open('setupdb/addequity.py').read()) 

from custodian.models import *
import datetime
import pandas as pd
eq=pd.read_csv("C:/Users/Dimuthu/Downloads/eq.csv",header=None,dtype={4:str}) 
eq['security_id'] = eq[[2,3,4]].agg('-'.join, axis=1)
for index,row in eq.iterrows():
  e = ListedEquity(ticker=row['security_id'],company_name=row[11],current_price=row[9],current_price_date=datetime.date.today(),in_sl20=False)
  e.save()


