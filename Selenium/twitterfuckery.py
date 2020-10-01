# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 21:00:54 2020

@author: Sam
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



def insta_search(username, password, searchterm ):
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(PATH) # determining browser and driver path
    driver.get('https://instagram.com/')
    
    username = str(username)
    password = str(password)
    searchterm = str(searchterm)
    
    time.sleep(3)
    
    search = driver.find_element_by_name('username')
    search.send_keys(username)
    
    search = driver.find_element_by_name('password')
    search.send_keys(password)
    
    search.send_keys(Keys.RETURN) # pressing enter button
    
    time.sleep(5)
    
    search = driver.find_element_by_class_name('sqdOP.yWX7d.y3zKF')
    search.click() 
    
    time.sleep(3)
    
    search = driver.find_element_by_class_name('aOOlW.HoLwm')
    search.click() 
    
    time.sleep(3)
    
    driver.get('https://instagram.com/explore/tags/' + searchterm + '/')
    
    
    
insta_search('sambodza@hotmail.co.uk', 'Onlyexception6', 'filmisnotdead')
