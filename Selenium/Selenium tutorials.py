# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 21:42:35 2020

@author: Sam
"""

'SELENIUM TUTORIAL'

### TUTORIAL 1

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = 'C:\Program Files (x86)\chromedriver.exe'

driver = webdriver.Chrome(PATH) # determining browser and driver path

# driver.get('https://www.google.com/webhp') # how to open webpage

# print('the title of the webpage is', driver.title) # finds webpage title

# time.sleep(3) # delays by 3s

# driver.close() # closes tab

# time.sleep(3)

# driver.quit() # closes browser

### TUTORIAL 2

# in chrome use right click and click inspect element, to find element in HTML code
# most common ways to access are using name, class or ID 
# use Id -> name -> class (most unique to least unique)

driver.get('https://techwithtim.net/') # how to open webpage

search = driver.find_element_by_name('s') # name of search bar

search.send_keys('test') # using keyboard

search.send_keys(Keys.RETURN) # pressing enter button

try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'main' ))
    )
    
    articles = main.find_elements_by_tag_name('article')
    for article in articles:
        header = article.find_element_by_class_name('entry-summary')
        print(header.text)

finally:
    driver.quit()
    
### TUTORIAL 3

driver = webdriver.Chrome(PATH)
driver.get('https://techwithtim.net/')

link = driver.find_element_by_link_text('Python Programming')
link.click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Beginner Python Tutorials' ))
    )
    #element.clear() # clears search fields
    element.click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'sow-button-19310003' ))
    )
    element.click()
    
    driver.back()
    driver.back()
    driver.back()
    driver.forward()
    driver.forward()
    
except:
    driver.quit()
    
### TUTORIAL 4

from selenium.webdriver.common.action_chains import ActionChains

PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH) # determining browser and driver path 
driver.get('https://orteil.dashnet.org/cookieclicker/')

time.sleep(5)

cookie = driver.find_element_by_id('bigCookie')
cookie_count = driver.find_element_by_id('cookies')

items = [driver.find_element_by_id('productPrice' + str(i)) for i in range(1,-1,-1)]

actions = ActionChains(driver)
actions.click(cookie)

for i in range(5000):
    actions.perform()
    count = int(cookie_count.text.split(' ')[0])
    for item in items:
        value = int(item.text)
        if value <= count:
            upgrade_actions = ActionChains(driver)
            upgrade_actions.move_to_element(item)
            upgrade_actions.click()
            upgrade_actions.perform()
            

            
     
            

        
