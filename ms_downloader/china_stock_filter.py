'''
Created on 20 Jul 2018

@author: Forrest.Li
'''
import good_morning as gm
import pandas as pd

stock_ticker='2006.hk'

kr = gm.KeyRatiosDownloader()
fr = gm.FinancialsDownloader()  
kr_frames = kr.download(stock_ticker) 
fr_frames = fr.download(stock_ticker)
print(fr_frames,kr_frames)
#fr_income_statement_frame=fr_frames['income_statement'].set_index('title')
#print(fr_income_statement_frame.loc['2015'])
#print (fr_income_statement_frame)
for yearnum in range(2015,2018):
    year = str(yearnum)
    print ('year', year)
    year_begin_date=year+'0101'
    year_end_date=year+'1231'

    continuing_net_income=fr_frames[year]['income_statement']['Net income from continuing operations']    
    print(f'continuing_net_income {continuing_net_income}')