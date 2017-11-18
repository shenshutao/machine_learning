#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# open main page
#driver = webdriver.Chrome('win_drivers/chroamedriver.exe')
driver = webdriver.Chrome('mac_drivers/chromedriver')
driver.implicitly_wait(10) # default
driver.get("https://www.tripadvisor.com.sg/")

# sumbit search
driver.find_element_by_css_selector("input.typeahead_input").clear()
driver.find_element_by_css_selector("input.typeahead_input").send_keys("marina bay sands")
driver.find_element_by_id("SUBMIT_HOTELS").click()

lastPageBtn = driver.find_element_by_css_selector("#taplc_location_reviews_list_hotels_0 > div > div.prw_rup.prw_common_north_star_pagination > div > div > span.pageNum.last.taLnk");

pageCount = lastPageBtn.get_attribute('data-page-number')
print(pageCount)

# Loop all pages
j=1
for i in range(1,int(pageCount)):
    print("================= Page " + str(i) + " ========================")
    try:
        # click more buttons
        WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "entry")));    
    
        moreBtn = driver.find_element_by_css_selector("div.entry p span")
        if moreBtn is not None:
            
                moreBtnClickable = WebDriverWait(driver, 20, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.entry p span")))
                moreBtnClickable.click(); # ajax load more content.
                WebDriverWait(driver, 20, 0.5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.entry span"), "Show less"))
            
        
        for link in driver.find_elements_by_class_name("review-container"):
            print(j)
            print(link.find_element_by_tag_name('p').text)
            
            j=j+1
            
    except: 
        print('Exception here ! Skip Page ' + str(i))
        pass

    # go to next page
    nextPageBtn = driver.find_element_by_css_selector("#taplc_location_reviews_list_hotels_0 > div > div.prw_rup.prw_common_north_star_pagination > div > span.nav.next.taLnk")
    nextPageBtn.click()