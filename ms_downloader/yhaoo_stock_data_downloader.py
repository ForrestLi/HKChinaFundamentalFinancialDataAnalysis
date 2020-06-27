'''
Created on 23 Feb 2018

@author: Forrest.Li
'''


from pandas_datareader import data as pdr

import fix_yahoo_finance as yf
yf.pdr_override() # <== that's all it takes :-)

# download dataframe
data = pdr.get_data_yahoo("000001.SS", start="2011-01-01", end="2017-04-30")
#print(data)
# download Panel
data = pdr.get_data_yahoo(["600820", "000001.SS"], start="2000-01-01", end="2017-04-30")
print(data)