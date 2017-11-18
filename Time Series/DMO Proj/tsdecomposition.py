#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 17:06:56 2017

@author: shutao
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# change working directory
os.chdir('/Users/shutao/Documents/GitHub/Machine-Learning/Time Series/DMO Proj')

# Define function test_stationarity 
from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries):
    
    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)
 
    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    #Perform Dickey-Fuller test:
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)

# load data
towngas=pd.read_excel('SingStat Data.xlsx')
towngas['date'] = [(pd.to_datetime(ss[0]) + pd.offsets.QuarterEnd(int(ss[1][0]))) for ss in towngas['Quarter'].str.split(' ')]
data = towngas[['date','TotTownGas_MKWH']]

# data plot
plt.plot(data['date'], data['TotTownGas_MKWH'])
data.head()
data.index = pd.DatetimeIndex(data['date'])


from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib import pyplot

ts = data['TotTownGas_MKWH']

	
test_stationarity(ts)

# Additive Model
print("Additive Model")
decomposition = seasonal_decompose(ts, model='additive')
decomposition.plot()
pyplot.show()

#print(result.trend)
#print(result.seasonal)
#print(result.resid)
#print(result.observed)


# Multiplicative Decomposition
print("Multiplicative Model")
decomposition2 = seasonal_decompose(ts, model='multiplicative')
decomposition2.plot()
pyplot.show()

#print(decomposition2.trend)
#print(decomposition2.seasonal)
#print(decomposition2.resid)
#print(decomposition2.observed)



