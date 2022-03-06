import json
import pandas as pd
import requests
import time
import logging
from random import randint
from time import sleep
import datetime
new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
from nsetools import Nse
nse=Nse()
def fetch_oi(current_strike,expiry_dt,dajs,look_back):
    ce_sum=[]
    pe_sum=[]
    price=current_strike-100*look_back
    ce_temp=0
    pe_temp=0
    ce_values = [data['CE'] for data in dajs['records']['data'] if "CE" in data and data['expiryDate'] == expiry_dt]
    pe_values = [data['PE'] for data in dajs['records']['data'] if "PE" in data and data['expiryDate'] == expiry_dt]
    ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])
    pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])
    while (price!=current_strike+100*(look_back+1)):
        ce_temp=ce_temp+ce_dt[ce_dt['strikePrice']==price]['changeinOpenInterest'].tolist()[0]
        pe_temp=pe_temp+pe_dt[pe_dt['strikePrice']==price]['changeinOpenInterest'].tolist()[0]
        #print(f"now ce_temp is {ce_temp} and pr_temp is {pe_temp} ")
        price=price+100
    ce_sum.append(ce_temp)
    pe_sum.append(pe_temp)
    temp=f"new value of call open interest change is {ce_sum[-1]} and put open interest change is {pe_sum[-1]}"
    temp=temp+f"now put to call ratio is {pe_sum[-1]/ce_sum[-1]}"
    pcr=ce_sum[-1]/pe_sum[-1]
    if (pcr>2):
        print(f"high put to call ratio")
    return temp
def max_oi(current_strike,expiry_dt,dajs,look_back):
    ce_sum=[]
    pe_sum=[]
    ce_values = [data['CE'] for data in dajs['records']['data'] if "CE" in data and data['expiryDate'] == expiry_dt]
    pe_values = [data['PE'] for data in dajs['records']['data'] if "PE" in data and data['expiryDate'] == expiry_dt]
    ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])
    pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])
    index=ce_dt.loc[ce_dt['strikePrice']==current_strike].index[0]
    a=ce_dt['strikePrice'].iloc[ce_dt['openInterest'].iloc[index-look_back:look_back+index+1].idxmax()]
    index=pe_dt.loc[pe_dt['strikePrice']==current_strike].index[0]
    b=pe_dt['strikePrice'].iloc[pe_dt['openInterest'].iloc[index-look_back:look_back+index+1].idxmax()]
    return f"maximum call writing OI strike price is {a} and maximum put writing OI strike price is {b}"
def get_page():
    checker=True
    while(checker):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            page = requests.get(new_url,headers=headers)
            page = json.loads(page.text)
            checker=False
            return page
        except:
            print("Exception")
def get_expiry_date():
    dajs=get_page()
    df=pd.to_datetime(pd.Series(dajs['records']['expiryDates']))
    df=df.sort_values()
    now=pd.to_datetime(datetime.datetime.now())
    if now<=df[0]:
        return df[0].strftime("%d-%b-%Y")
    if now>df[0]:
        return df[1].strftime("%d-%b-%Y")
def call_put_ratio_bnf():
    nse=Nse()
    look_back=5
    expiry_dt = get_expiry_date()
    current_strike=int(round(nse.get_index_quote('nifty bank')['lastPrice'],ndigits=-2))
    dajs=get_page()
    a=fetch_oi(current_strike,expiry_dt,dajs,5)
    b=max_oi(current_strike,expiry_dt,dajs,5)
    return a,b
    