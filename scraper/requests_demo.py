
# coding: utf-8

# In[1]:

import requests


# In[2]:

url = 'http://www.omdbapi.com/?apikey=<need pay>&t=Wolf Warrior'


# In[3]:

r = requests.get(url)


# In[24]:

r.text


# In[8]:

json_data = r.json()


# In[22]:

for k in json_data.keys():
    print(k + ': ', json_data[k])


# In[23]:

json_data

