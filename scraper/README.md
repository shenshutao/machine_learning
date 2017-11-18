# Scrapers
Website scraper - Python

# Demos from text mining class - yuhao,zhenzhen
- from_file_demo.py
- requests_demo.py
- beautifulsoup_demo1.py
- beautifulsoup_demo2.py

# Selenium Demo - shutao
- selenium_demo.py      
For the website which have complex behaviors such as JavaScript, Ajax, Login ...     
Use selenium will browser the website as human did.    

#### Something maybe useful:     
Three types of wait in selenium             
- Force waits (not good)
    - sleep time too short might be not enough for page loading. 
    - sleep time too long affect the performance.
```
from time import sleep
# Force the thread sleep 10s to wait for page loading
sleep(10)
```

- Implicit Waits      
Go to next step until the whole page is fully loaded.
    - sometime we only need the page partial loaded.
    - seems only work for driver.get, not for click redirection.
```
driver.implicitly_wait(30) # seconds
driver.get("http://somedomain/url")
```
    
- Explicit Waits (best, but a bit bother)    
Define the expected condition, go to the next step only the expected condition is fulfilled, otherwise throw TimeoutException based on the timeout parameter.         
```
from selenium.webdriver.support import expected_conditions as EC

# check if the expected condition is fulfilled every 0.5s, if it is 
# fulfilled, go to next step. 
# if waiting time exceed 20s, throw TimeoutException.
WebDriverWait(driver, 20, 0.5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "entry")));    
```
Detials for expected condition: https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html


