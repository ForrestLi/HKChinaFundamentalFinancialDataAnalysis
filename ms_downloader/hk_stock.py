'''
Created on 3 Jul 2018

@author: Forrest.Li
'''
import chinastock as cs
import good_morning as gm
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn
#from _overlapped import NULL
import logging

#seaborn.set(style='ticks')
def book_value_filter(stock_ticker,bv_filter=0.5):
    bv_list = []
    kr = gm.KeyRatiosDownloader()
    kr_frames = kr.download(stock_ticker) 
    logging.INFO(f'{kr_frames}')
    for yearnum in range(2008,2018):
        year = str(yearnum)
        key_ratiostatements = kr_frames[0][year].dropna()
        
        book_value=key_ratiostatements.filter(regex='Book Value Per Share')

        if book_value:
            bv_list.append(book_value)
    return bv_list

def roe_filter (stock_ticker, roe_threshold=20):
  kr = gm.KeyRatiosDownloader()
  #fr = gm.FinancialsDownloader()  
  kr_frames = kr.download(stock_ticker) 
  #fr_frames = fr.download(stock_ticker)
  #print(fr_frames)
  #print (kr_frames)
  roe_list = []
  for yearnum in range(2008,2018):
    year = str(yearnum)
    #book_value=kr_frames[0][year]['Book Value Per Share * HKD']   
    #print(f'Book value{book_value}')
    key_ratiostatements = kr_frames[0][year].dropna()
    key_profitabilityRatioStatements = kr_frames[2][year].dropna()
    #print( key_ratiostatements)
    #financial_ratiostatements = fr_frames[0][year]
    eps=[value for key, value in key_ratiostatements.items() if 'Earnings Per Share' in key]
    #print (f'year {year} eps {eps}')
    roe = [value for key, value in key_profitabilityRatioStatements.items() if 'Return on Equity' in key]

    #print (f'year {year} roe {roe}')
    if roe != []:
       roe_list.append(roe[0])
  sum = 0
  count =0 
  for i in roe_list:
    sum = sum + i
    count = count + 1
    average_roe=sum/count       
  #print (roe_list, average_roe)
  if average_roe > roe_threshold:
     return average_roe
  else:
     return False

def worker (self):
    for i in range(1,9999):
     i = str(i).zfill(4)
     stock_ticker='XHKG:0'+i
     LOG.info(f'stock_ticker: {stock_ticker}')
     try:
       roe_value=roe_filter(stock_ticker)
       if roe_value:
          LOG.info(stock_ticker, roe_value)
     except:
        pass
 
if __name__ == '__main__':
  LOG = logging.getLogger()
  logging.basicConfig(
        format='%(levelname)s/%(module)s:%(lineno)d: %(message)s',
        level=logging.INFO)
  bv_list = book_value_filter('XHKG:02006')
  logging.INFO(f'{bv_list}')
  #worker()    

        #print (f'no value found for {stock_ticker}' )
       



