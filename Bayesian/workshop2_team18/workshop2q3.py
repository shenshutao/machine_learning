#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 18:33:46 2017

@author: shutao
"""
import json
import requests
import pickle as pk
from os import chdir

from utility import pre_process


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode
    
# change workspace
folder_path = "/Users/shutao/Desktop/Sentiment Mining/workshops/Day 2/Data"
chdir(folder_path) 

# OAuth credential placeholders that must be filled in by users.
CLIENT_ID = "CPkDgGzpo5nwIWuJCXUzlw"
CLIENT_SECRET = "lgkH0kT0MC9GfuuHm8ylntwuJS5Qeij6PzxoIyukL64SA91FLLbM9SwupwfY6A6a"

# API constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token


def requestAPI(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    print ("url_params are " + str(url_params))
    
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def recordBusinessID(category, searchResp):
   for business in searchResp['businesses']:
       print(business['id'])
       nb_review = int(business['review_count'])
       if(nb_review >= 3):
           businessId = business['id']
           
           path="/v3/businesses/"+ businessId + "/reviews"
           result = requestAPI(API_HOST, path, bearer_token)
           if(len(result['reviews']) >= 3):
               reviewAndScoreList = []
               for review in result['reviews']:
                   data_ready = pre_process(review['text'])
                   predNB = classifier_nb.predict([data_ready])            
                   reviewAndScoreList.append({"text": review['text'], "score": int(predNB[0] == 'positive')})
               
               businessIDs[category].append(
                   {"name" : businessId,
                   "nb_reviews" :nb_review,
                   "reviews" : reviewAndScoreList
                   })
       

# prepare
bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

classifier_nb = pk.load(open("classifier_nb.pk", "rb"))
categories = ['singaporean','french','japanese','korean','indpak']

businessIDs = {}

for category in categories:
    businessIDs[category] = []
    url_params = {
            'location': 'singapore',
            'categories': category,
            'offset': 0,
            'limit': 50
        }
    result = requestAPI(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)    
    total = result['total']
    print('Total is ', total)
    
    recordBusinessID(category, result)
        
    offset = 50
    while (offset < total):
        url_params['offset'] = offset
        result = requestAPI(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)
        recordBusinessID(category, result)
        offset += 50
        

print("Save into file")
with open('yelp_review.json', 'w') as outfile:  
    json.dump(businessIDs, outfile, indent=4)
 
        
    
    
