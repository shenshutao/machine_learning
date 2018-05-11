#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json

os.chdir("/Users/shutao/Desktop/Big Data Engineering For Analytics/BDA - spider")
#
# countryList = dict()
# countryList['Indonesia'] = {"url": "https://www.tripadvisor.com.sg/Tourism-g294225-Indonesia-Vacations.html", 'dest_no': 6}
# countryList['Malaysia'] = {"url": "https://www.tripadvisor.com.sg/Tourism-g293951-Malaysia-Vacations.html", 'dest_no': 6}
# countryList['China'] = {"url": "https://www.tripadvisor.com.sg/Tourism-g294211-China-Vacations.html", 'dest_no': 12}
# countryList['India'] = {"url": "https://www.tripadvisor.com.sg/Tourism-g293860-India-Vacations.html", 'dest_no': 12}
# countryList['Philippines'] = {"url": "https://www.tripadvisor.com.sg/Tourism-g294245-Philippines-Vacations.html", 'dest_no': 6}
# countryList['Japan'] = {"url": "https://www.tripadvisor.com.sg/Tourism-g294232-Japan-Vacations.html", 'dest_no': 6}
# countryList['Nepal'] = {"url": "https://www.tripadvisor.com.sg/Tourism-g293889-Nepal-Vacations.html", 'dest_no': 6}
# countryList['Laos'] = {"url": "https://www.tripadvisor.com.sg/Tourism-g293949-Laos-Vacations.html", 'dest_no': 6}
# countryList['Cambodia'] = {"url": "https://www.tripadvisor.com.sg/Tourism-g293939-Cambodia-Vacations.html", 'dest_no': 6}
# countryList['Myanmar'] = {"url": "https://www.tripadvisor.com.sg/Tourism-g294190-Myanmar-Vacations.html", 'dest_no': 6}
# # countryList['Singapore'] = "https://www.tripadvisor.com.sg/Attractions-g294265-Activities-Singapore.html"
#
#
# print("Save into file")
# with open('lonelyplanet_country_list.json', 'w') as outfile:
#     json.dump(countryList, outfile, indent=4)
#
# # -------------------- stage 1 -----------------------
#
# with open('lonelyplanet_country_list.json') as json_data:
#     countryList2 = json.load(json_data)
#
# for key, value in countryList2.items():
#     print(key)
#     url = value.get('url')
#     dest_no = value.get('dest_no')
#
#     # open main page
#     # driver = webdriver.Chrome('win_drivers/chroamedriver.exe')
#     driver = webdriver.Chrome('mac_drivers/chromedriver')
#     driver.implicitly_wait(10)  # default
#     driver.get(url)
#
#     EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.popularCities"), '#1')
#
#     clickTimes = dest_no // 6
#     for num in range(1, clickTimes):
#         driver.find_element_by_css_selector("#BODYCON > div:nth-child(2) > div > div > div.morePopularCitiesWrap > div").click()
#         EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.popularCities"), "#"+str(num*6+1))
#
#     time.sleep(3)
#     div = driver.find_element_by_css_selector("#BODYCON > div:nth-child(2) > div > div > div.popularCities")
#     dest_list = []
#     for tag in div.find_elements_by_tag_name('a'):
#         dest = dict()
#         try:
#             dest['name'] = tag.find_element_by_class_name('name').text
#             dest['rankNum'] = tag.find_element_by_class_name('rankNum').text
#             dest['url'] = tag.get_attribute('href')
#             print(key, ' ', dest['name'])
#             dest_list.append(dest)
#         except Exception as e:
#             print(e)
#
#     value['dest'] = dest_list
#
# print("Save into file 2")
# with open('lonelyplanet_country_destion.json', 'w') as outfile:
#     json.dump(countryList2, outfile, indent=4)

# -------------------- stage 2 -----------------------

import urllib.request
from bs4 import BeautifulSoup

base_url = "https://www.tripadvisor.com.sg"
def get_page(uri):
    url = base_url + uri
    req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"})
    resp = urllib.request.urlopen(req)
    soup = BeautifulSoup(resp, "html.parser")
    return soup

with open('lonelyplanet_country_destion.json') as json_data:
    countryList3 = json.load(json_data)

# driver = webdriver.Chrome('win_drivers/chroamedriver.exe')
driver = webdriver.Chrome('mac_drivers/chromedriver')
driver.implicitly_wait(10)  # default

for key, value in countryList3.items():
    print(key)
    print(value['dest'])
    for dest in value['dest']:
        driver.get(dest['url'])
        driver.find_element_by_link_text('Browse all things to do').click()

        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.ap_filter_header"), "Types of Things to Do")
        bs_page = BeautifulSoup(driver.page_source, "html.parser")

        data = dict()

        attraction_list = bs_page.find("div", {"class": "attraction_list"})
        for attraction in attraction_list.find_all("div", {"class": "attraction_element"})[:5]:
            attraction_dict = {}
            title_div = attraction.find("div", {"class": "listing_title"})
            title = title_div.text.strip()
            attraction_dict["title"] = title

            href = title_div.a["href"].strip()
            attraction_dict["href"] = base_url + href

            rating = attraction.find("div", {"class": "listing_rating"})
            rank_div = rating.find("div", {"class": "rs rating"})
            rating_score = rank_div.span["alt"].strip()
            attraction_dict["rating"] = rating_score

            review_span = rating.find("span", {"class": "more"})
            review_number = review_span.text.strip()
            attraction_dict["review_number"] = review_number

            things_to_do_page = get_page(href)
            reviews = []
            for review in things_to_do_page.find_all("p", {"class": "partial_entry"}):
                reviews.append(review.text.strip())

            attraction_dict["reviews"] = reviews

            data[title] = attraction_dict
        dest['thing_to_do'] = data

print("Save into file 3")
with open('lonelyplanet_country_destion_activities.json', 'w') as outfile:
    json.dump(countryList3, outfile, indent=4)



# driver.close()



# lastPageBtn = driver.find_element_by_css_selector(
#     "#taplc_location_reviews_list_hotels_0 > div > div.prw_rup.prw_common_north_star_pagination > div > div > span.pageNum.last.taLnk");
#
# pageCount = lastPageBtn.get_attribute('data-page-number')
# print(pageCount)
#
# # Loop all pages
# j = 1
# for i in range(1, int(pageCount)):
#     print("================= Page " + str(i) + " ========================")
#     try:
#         # click more buttons
#         WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "entry")));
#
#         moreBtn = driver.find_element_by_css_selector("div.entry p span")
#         if moreBtn is not None:
#             moreBtnClickable = WebDriverWait(driver, 20, 0.5).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, "div.entry p span")))
#             moreBtnClickable.click();  # ajax load more content.
#             WebDriverWait(driver, 20, 0.5).until(
#                 EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.entry span"), "Show less"))
#
#         for link in driver.find_elements_by_class_name("review-container"):
#             print(j)
#             print(link.find_element_by_tag_name('p').text)
#
#             j = j + 1
#
#     except:
#         print('Exception here ! Skip Page ' + str(i))
#         pass
#
#     # go to next page
#     nextPageBtn = driver.find_element_by_css_selector(
#         "#taplc_location_reviews_list_hotels_0 > div > div.prw_rup.prw_common_north_star_pagination > div > span.nav.next.taLnk")
#     nextPageBtn.click()
