
# coding: utf-8

# In[1]:

import urllib
import urllib.request

from bs4 import BeautifulSoup


# In[2]:

theurl="https://twitter.com/realDonaldTrump"


# In[3]:

thepage=urllib.request.urlopen(theurl)


# In[4]:

soup=BeautifulSoup(thepage, "html.parser")


# In[6]:

i=0
for link in soup.find_all('a'):
    #print(link.get('href'))
    print(i)
    print(link)
    print(link.text)
    
    i=i+1


# In[9]:

j=1
for link in soup.find_all("div", {"class":"js-tweet-text-container"}):
    print(j)
    print(link.text)
    
    j=j+1


# In[11]:

soup


# In[13]:

thepage


# In[14]:

soup.title


# In[15]:

soup.title.string


# In[16]:

i


# In[ ]:



