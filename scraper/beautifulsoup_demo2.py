
# coding: utf-8

# In[1]:

import urllib
import urllib.request

from bs4 import BeautifulSoup


# In[3]:

theurl="https://www.tripadvisor.com.sg/Hotel_Review-g294265-d301583-Reviews-Raffles_Hotel_Singapore-Singapore.html"


# In[4]:

def make_soup(url):
    thepage=urllib.request.urlopen(url)
    soupdata=BeautifulSoup(thepage,"html.parser")
    return soupdata


# In[13]:

def add_five(x):
    y=x+5
    return y


# In[14]:

add_five(5)


# In[7]:

soup=make_soup(theurl)


# In[8]:

print(soup.prettify())


# In[9]:

j=1
for link in soup.find_all("div",{"class":"review-container"}):
    print(j)
    print(link.find('p').text)
    
    j=j+1


# In[10]:

for m in [1,2,3,5,6]:
    print(m)


# In[33]:

j=1
for link in soup.find_all("div",{"class":"rating reviewItemInline"}):
    print(j)
    print(link)
    print(link.find_all('span')[0])
    print(link.find_all('span')[0].attrs['class'][1])
    print(link.find_all('span')[1].attrs['title'])
    j=j+1


# In[15]:

j=1
set1=[]
for link in soup.find_all("div",{"class":"review-container"}):
    set1.append(link.find('p').text)
    j=j+1
    
print(type(set1),len(set1))


# In[27]:

set2=[]
set3=[]
j=1
for link in soup.find_all("div",{"class":"rating reviewItemInline"}):
    set2.append(link.find_all('span')[0].attrs['class'][1])
    set3.append(link.find_all('span')[1].attrs['title'])
    j=j+1
    
print(type(set2),len(set2))
print(type(set3),len(set3))


# In[28]:

import pandas as pd
df = pd.DataFrame({'c1': set1,
                  'c2': set2,
                  'c3':set3})
df.head()


# In[29]:

df.columns = ['Review','Rate','Date']


# In[30]:

df.head()


# In[ ]:



