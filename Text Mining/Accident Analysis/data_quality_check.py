#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 10:55:42 2017

@author: shutao
"""

import os
import pandas
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

# change working directory
os.chdir('/Users/shutao/Documents/GitHub/Machine-Learning/Text Mining/Accident Analysis/question & original data')

# load data
msia_data = pd.read_excel("MsiaAccidentCases.xlsx")
osha_data = pd.read_excel("osha.xlsx", header = None, index_col=0, 
                          names=["Title Case", "Details","Summary Case","Remarks"])

print(msia_data.shape)
print(msia_data.describe())
print(msia_data['Cause '].unique())

print(osha_data.shape)
print(osha_data.describe())

############################ do data cleaning manually #####################
os.chdir('/Users/shutao/Documents/GitHub/Machine-Learning/Text Mining/Accident Analysis/clean data')

# load data after cleaning
msia_data_after = pd.read_csv("MsiaAccidentCases.csv")
print(msia_data_after.shape)
print(msia_data_after.describe())

categories_count = Counter(msia_data_after["Cause"])
df = pandas.DataFrame.from_dict(categories_count, orient='index')
df.plot(kind='barh')
print(categories_count)



