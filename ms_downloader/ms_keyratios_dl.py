'''
Created on 12 Feb 2018

@author: Forrest.Li
'''
import good_morning as gm
import re
from _overlapped import NULL
import sys

def get_roe(stock_ticker):
    roe_matcher = '.*Return on Equity.*'
   
    kr = gm.KeyRatiosDownloader()
    fr = gm.FinancialsDownloader()
    try:
        kr_frames = kr.download(stock_ticker)
        fr_frames = fr.download(stock_ticker)
        roe=re.findall(roe_matcher, str(kr_frames[2]))
        print('doc',kr_frames[2]['2017']['Return on Equity %'])
        print(stock_ticker,'orginal kr',kr_frames)
        print(stock_ticker,'oringal fr',fr_frames)
        #print('tranpos',kr_frames[2].transpose())
    except Exception as novalue:
        #print (f'got Exception {sys.exc_info()}')
        roe=NULL
    return roe

def roe_calculator(roestring):
    digit_matcher = '.*\d+.*'
    roe_list= roestring.split(' ') 
    #print(roe_list)
    roe_value_list=[]
    for i in roe_list:
        find_value=re.search(digit_matcher, i)
        if find_value !=None:      
       #print(find_value.group(0))
           roe_value_list.append(find_value.group(0))
    total_roe=0
    counter=0
    for i in roe_value_list:
        total_roe=total_roe+float(i)
        counter=counter+1
    #print('average roe:',total_roe/counter)
    if counter==0:
        return NULL    
    return total_roe/counter

shenzhen_ticker_list=[]
ticker = 1000000
#hk one         100000
#sz one         1000000
while (ticker < 1001000):
    shenzhen_ticker_list.append(str(ticker)[1:])
    ticker=ticker+1

for i in shenzhen_ticker_list:
    #print(f'trying to fetech data for stock {i}')
    roe=get_roe(str(i))
    if roe!=NULL:
       pre5roe=roe_calculator(roe[0])
    #print(pre5roe)
       later3roe=roe_calculator(roe[1])
       if(pre5roe!=NULL and later3roe!=NULL):
    #print(later3roe)
         if(pre5roe>20 and later3roe>20): 
              print('ticker with roe>30:', i)
              print('pre5roe',pre5roe)
              print('later3roe',later3roe)
#fr =  gm.FinancialsDownloader()
#fr_frames = fr.download('600820')
#print(fr_frames)