'''
Created on 20 Apr 2020

@author: Forrest.Li
'''

def vaid_shenzhen_ticker_yielder():
    for i in range(1000001,1001000):
        yield str(i)[1:]

def vaid_techboard_ticker_yielder():
    for i in range(1300001,1301000):
        yield str(i)[1:]

def vaid_shanghai_ticker_yielder():
    for i in range(1600001,1603000):
        yield str(i)[1:]

def vaid_hk_ticker_yielder():
      for i in range(100001,104999):
        yield 'XHKG:'+str(i)[1:]
def test_ticker():
        for i in vaid_hk_ticker_yielder():
            print (i) 
            
            
test_ticker()