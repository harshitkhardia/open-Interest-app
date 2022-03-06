from django.http import HttpResponse
from django.shortcuts import render
import os
from .oi_functions import * 
def index(request):
    print("harshit")
    a,b=call_put_ratio_bnf()
    expiry_date=str(get_expiry_date())
    current_strike=int(round(nse.get_index_quote('nifty bank')['lastPrice'],ndigits=-2))
    params={'value1':a,'value2':b,'expiry':expiry_date,'current_strike':current_strike}
    return render(request,'templates\index.html',params)
def about(request):
    #s=f"<h1>you are in about <br> {b}</h1>"
    return HttpResponse("hsrsihsof")

def CurrentDateTime(request):
    time=datetime.datetime.now
    html="<html><body>It is now %s.</body></html>" % time
    return HttpResponse(html)
