"""

Script for auto updating a facebbok page


search google news for 'dentistry UK'
using: https://www.google.com/search?q=dentistry+uk&hl=en&sxsrf=ALeKk01Ds170v8PIq2dFVvkWfoyllX5y7g:1601197315311&source=lnms&tbm=nws&sa=X&ved=2ahUKEwivysbp_IjsAhVEiFwKHQZLCTMQ_AUoAnoECAwQBA&biw=1745&bih=888



"""
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from datetime import date

def small_menu_select(ID,key,times):
    search = driver.find_element_by_id(str(ID))
    search.click()
    for i in range(times): search.send_keys(str(key)) 
    search.send_keys(Keys.RETURN)
    
def findby_id_click(ID):
    search = driver.find_element_by_id(ID)
    search.click()
    
def findby_id_keys(ID,msg):
    search = driver.find_element_by_id(ID)
    search.send_keys(msg)
    
def findby_xpath_click(xpath):
    search = driver.find_element_by_xpath(xpath)
    search.click()
    
def findby_xpath_keys(xpath,msg):
    search = driver.find_element_by_xpath(xpath)
    search.send_keys(msg)
    
def findby_xpath_ENTER(xpath):
    search = driver.find_element_by_xpath(xpath)
    search.send_keys(Keys.ENTER)


#############################################################################

### YOUR VARIABLES ###

FILEPATH = 'C:/Users/Sam/Documents/Python Projects/Selenium/'
# change this to wherever you want to save the csv and word file to

PATH = 'C:\Program Files (x86)\chromedriver.exe'
# path to chrome driver

fb_login = 'yourusername'
fb_pass = 'yourpassword'
search_term = 'yoursearchterm'

#############################################################################

### Setup


search_term = search_term.split(' ')
search_term = str('+'.join(search_term))

link = 'https://www.google.com/search?q='+ search_term +'&hl=en&sxsrf=ALeKk01Ds170v8PIq2dFVvkWfoyllX5y7g:1601197315311&source=lnms&tbm=nws&sa=X&ved=2ahUKEwivysbp_IjsAhVEiFwKHQZLCTMQ_AUoAnoECAwQBA&biw=1745&bih=888' # searched google news


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(PATH, chrome_options=chrome_options) # open browser

driver.get(link) # go to link

time.sleep(1) 

search = driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/g-card/div/div/div[2]/a/div')

title = search.find_element_by_xpath('//*[@id="rso"]/div[1]/g-card/div/div/div[2]/a/div/div[2]/div[2]').text
body = search.find_element_by_xpath('//*[@id="rso"]/div[1]/g-card/div/div/div[2]/a/div/div[2]/div[3]/div[1]').text # grabs all the releavnt stuff from the panel
link = search.find_element_by_xpath('//*[@id="rso"]/div[1]/g-card/div/div/div[2]/a').get_attribute('href')

driver.close()

driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
driver.get('https://www.facebook.com/')

time.sleep(1)

findby_id_keys('email', fb_login)
findby_id_keys('pass', fb_pass)
findby_xpath_click('//*[@id="u_0_d"]') # login
time.sleep(2)
findby_xpath_click('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[1]/div/div/div/div/div[3]/div[3]/ul/li[1]/a/div') # pages button
time.sleep(5)

findby_xpath_click('//*[@id="page_browser_your_pages"]/div/div[2]/div[1]/div[1]/div/div[1]/a') # click on page you want (can change xpath)
time.sleep(5)

post = title + '/n' + body + '/n' + link
post = post.replace('/n', Keys.ENTER)

search = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/form/div[1]/div/div[2]/textarea')
search.send_keys(post)

time.sleep(2)

findby_xpath_click('/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[3]/div[2]/div[2]/div/button/span')
