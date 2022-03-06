import django
import requests
import json
from random import randint
from time import sleep
from nsetools import Nse
from mysite.oi_functions import fetch_oi,max_oi
new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
def get_page():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(new_url,headers=headers)
        page = json.loads(page.text)
        if(page.status_code!=200):
            while(page.status_code!=200):
                sleep(randint(1,3))
                page = requests.get(new_url,headers=headers)
                #print(str(page.status_code)+'/n')
        return page
    except:
        sleep(randint(1,3))
        get_page()
def call_put_ratio_bnf():
    nse=Nse()
    look_back=5
    expiry_dt = '28-Oct-2021'
    current_strike=int(round(nse.get_index_quote('nifty bank')['lastPrice'],ndigits=-2))
    dajs=get_page()
    a=fetch_oi(current_strike,expiry_dt,dajs,5)
    b=max_oi(current_strike,expiry_dt,dajs,5)
    return a,b
    
if __name__=="__main__":
  a,b=call_put_ratio_bnf()
  print("hrhissdf")