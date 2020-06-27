'''
Created on 23 Feb 2018

@author: Forrest.Li
'''
import chinastock as cs
import good_morning as gm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
seaborn.set(style='ticks')

stock_ticker='600598'
#stock_ticker='3399'
#stock_ticker='0008'
#year='2016'
preYearEPS=1
simpleEPSGrowth=[]
stock_data_time_dic=dict((i[0], i[1])  for i in cs.get_stock_history(code=stock_ticker,exchange='SS'))
    #print(stock_data_time_dic['20161230'])
    #print(stock_data_time_dic)
stock_pd=pd.DataFrame(list(stock_data_time_dic.items()), columns=['Date', 'Price']) 
moving_average_20d=stock_pd.rolling(window=20).mean()
moving_average_200d=stock_pd.rolling(window=20).mean()

#fig = plt.figure()
#ax = fig.add_subplot(1,1,1)
#ax.plot(stock_pd.index, stock_pd, label=stock_ticker)
#ax.plot(moving_average_20d.index, moving_average_20d, label='20 days rolling')
#ax.plot(moving_average_200d.index, moving_average_200d, label='200 days rolling')
#ax.set_xlabel('Date')
#ax.set_ylabel('Adjusted closing price ($)')
#ax.legend()
kr = gm.KeyRatiosDownloader()
fr = gm.FinancialsDownloader()  
kr_frames = kr.download(stock_ticker) 
fr_frames = fr.download(stock_ticker)
#print(kr_frames, fr_frames) 
for yearnum in range(2008,2018):
    year = str(yearnum)
    print ('year', year)
    #print(cs.get_stock_today(code='000001', exchange='SS'))
    #print(cs.get_stock_history_adj(code='600820',exchange='SS'))
    #print(cs.get_stock_history(code='600820',exchange='SS'))
    year_begin_date=year+'0101'
    year_end_date=year+'1231'
    #stock price related sectio
    mask = (stock_pd['Date'] > year_begin_date) & (stock_pd['Date'] <= year_end_date)
    mean_price=stock_pd.loc[mask]['Price'].mean()
    max_price =stock_pd.loc[mask]['Price'].max()
    min_price =stock_pd.loc[mask]['Price'].min()
    #print(stock_pd.loc[mask])
    print(f'mean:{mean_price}')
    print(f'max:{max_price}', )
    print(f'min:{min_price}', )
    '''
    eps=kr_frames[0][year]['Earnings Per Share CNY']
    print(f'Earnings Per Share CNY{eps}')
    eps_growth=eps/preYearEPS-1
    eps_avg=0
    print(f'Earnings Growth Rate {eps_growth}')
    if(len(simpleEPSGrowth)<5):
        simpleEPSGrowth.append(eps_growth)
        print(simpleEPSGrowth)
        sum = 0
        for i in simpleEPSGrowth:
            sum = sum + i
        eps_avg = sum/len(simpleEPSGrowth)
    else:
        simpleEPSGrowth.pop(0)
        print(simpleEPSGrowth)
        sum = 0
        for i in simpleEPSGrowth:
            sum = sum + i
        eps_avg = sum/len(simpleEPSGrowth)
    print(f'eps_avg {eps_avg}')
    innerValue=(8.5+100*eps_avg)*eps
    print(f'innerValue: {innerValue}')
    maxInnerRatio=max_price/innerValue
    minInnerRatio=min_price/innerValue
    meanInneRatio=mean_price/innerValue
    print(f'year {year} maxInnerRatio {maxInnerRatio} minInnerRatio {minInnerRatio} meanInneRatio {meanInneRatio}')
    preYearEPS=eps
    maxPE=max_price/eps
    minPE=min_price/eps
    meanPE=mean_price/eps
    print(f'year {year} maxPE {maxPE} minPE {minPE} meanPE {meanPE}')
    '''
    book_value=kr_frames[0][year]['Book Value Per Share * CNY']
    
    print(f'Book value{book_value}')
    maxPB=max_price/book_value
    minPB=min_price/book_value
    meanPB=mean_price/book_value
    print(f'year {year} maxPB {maxPB} minPB {minPB} meanPB {meanPB}')

#print('doc',kr_frames[2]['2016']['Return on Equity %'])