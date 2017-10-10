#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 17:06:56 2017

@author: shutao
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima_model import ARIMA

# change working directory
os.chdir('/Users/shutao/Desktop/DMO Proj')

# load data
towngas=pd.read_excel('SingStat Data.xlsx')
towngas['date'] = [(pd.to_datetime(ss[0]) + pd.offsets.QuarterEnd(int(ss[1][0]))) for ss in towngas['Quarter'].str.split(' ')]
data = towngas[['date','TotTownGas_MKWH']]

# data plot
plt.plot(data['date'],data['TotTownGas_MKWH'])
data.head()
data.index = pd.DatetimeIndex(data['date'])

# we can see there is a clear trend.
acf(data['TotTownGas_MKWH'])



# build the model
model = ARIMA(data['TotTownGas_MKWH'], order=(5,1,0))
model_fit = model.fit(disp=0)
print(model_fit.summary())

