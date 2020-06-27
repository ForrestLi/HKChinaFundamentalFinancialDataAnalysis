#!/usr/bin/python
# -*- coding: utf-8 -*-


#from unittest import TestCase
import time

import pymysql
from good_morning import good_morning as gm

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASS = 'A1234567'
DB_NAME = 'ms_financials_db'

conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS, db=DB_NAME)

kr = gm.KeyRatiosDownloader()
fd = gm.FinancialsDownloader()

#class TestDownloadReturns(TestCase):
#class TestDownloadReturns():
def vaid_shenzhen_ticker_yielder():
    for i in range(1000001,1011980):
        yield str(i)[1:]

def vaid_techboard_ticker_yielder():
      for i in range(1300001,1301000):
        yield str(i)[1:]
        
def vaid_b_ticker_yielder():
      #for i in range(1200002,1201000):
      for i in range(1201000,1202000):
        yield str(i)[1:]

def vaid_shanghai_ticker_yielder():
#      for i in range(1600001,1603000):
      for i in range(1601010,1603000):
        yield str(i)[1:]
        
#def vaid_hk_ticker_yielder():
#      for i in range(100001,199999):
#        yield str(i)[1:]
        
def vaid_hk_ticker_yielder():
      for i in range(103613,103614):
        yield 'XHKG:'+str(i)[1:]
        
high_roe_15_dic={}
#vaid_shenzhen_ticker_yielder(),
#vaid_techboard_ticker_yielder(),
#need to add b ticker
#vaid_shanghai_ticker_yielder()
def test_download():
    for yielder in [ vaid_hk_ticker_yielder()]:
      for ticker in yielder:            
         try:
             kr_frames = kr.download(ticker)
             mean_roe = kr_frames[2].loc['Return on Equity %'].mean()
             print(high_roe_15_dic)
             print(f'processed {ticker}')
             #print(kr_frames[2])
             if(mean_roe >1):
                high_roe_15_dic[ticker] = mean_roe
                print(f'{ticker} has mean_roe {mean_roe}') 
                kr.download(ticker, conn)
                time.sleep(1)
                fd.download(ticker, conn)
                time.sleep(1)
                print(' ... success')
         except Exception as e:
                print(' ... failed', e)
      #print(high_roe_15_dic)       


test_download()


