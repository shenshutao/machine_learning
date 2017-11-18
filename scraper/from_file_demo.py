
# coding: utf-8

# In[1]:

file=open('moby_dick.txt', mode='r')


# In[2]:

print(file.read())


# In[3]:

print(file.closed)


# In[4]:

file.close()


# In[8]:

with open('moby_dick.txt') as file:
    print(file.readline())
    print(file.readlines()[6:8])


# In[9]:

with open('moby_dick.txt') as file:
    print(file.readline())
    book=file.readlines()


# In[10]:

len(book)


# In[14]:

import pandas as pd
file = 'titanic.csv'
df = pd.read_csv(file)
print(df)


# In[16]:

df.head()


# In[27]:

pd.DataFrame.hist(df.ix[:,4:5])


# In[28]:

import matplotlib.pyplot as plt
plt.show()

