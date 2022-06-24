from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import time
import urllib.request
import os
import pandas as pd
from urllib.parse import quote_plus          
from bs4 import BeautifulSoup as bs 
from xvfbwrapper import Xvfb
import time
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
import re
from selenium.webdriver.chrome.service import Service
import os 
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import pdb
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json



def accord_element(driver, xpath_data):
    text = []
    ratio = []
    pdb.set_trace()
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['accord_grid'])))
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_data['accord_grid'])))

        grid = driver.find_element(by = By.XPATH, value = xpath_data['accord_grid'])
        num = len(grid.find_elements(by = By.CLASS_NAME, value = 'accord-bar'))

        for i in range(1,num+1):
            try:
                xpath_f = xpath_data['accord_bar_f']
                xpath_b = xpath_data['accord_bar_b']
                xpath = xpath_f + str(i) + xpath_b
                
                accord = driver.find_element(by = By.XPATH, value = xpath)
                accord_text = accord.get_attribute("textContent")
                accord_score = accord.get_attribute("style")
                print(accord_text)
                text.append(accord_text)
                ration.append(accord_score)

            except NoSuchElementException:
                continue

        return text, ratio
    except TimeoutException:
        return None, None
    

def review_element(driver, xpath_data):
    score = []
    ratio = []
    pdb.set_trace()
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['review_grid'])))
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_data['review_grid'])))

        for i in range(1,6):
            try:
                xpath_f = xpath_data['review_score_f']
                xpath_b = xpath_data['review_score_b']
                xpath = xpath_f + str(i) + xpath_b
                
                review_score = driver.find_element(by = By.XPATH, value = xpath)
                bar = review_score.get_attribute("style")
       
                score.append(6-i)
                ratio.append(ratio)

            except NoSuchElementException:
                continue

        return score, ratio
    except TimeoutException:
        return None, None

def season_element(driver, xpath_data):

    ratio = []
    pdb.set_trace()
    season = ['winter','spring','summer','fall','day','night']
    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['season_grid'])))
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_data['season_grid'])))
        for i in range(1,7):
            try:
                xpath_f = xpath_data['season_score_f']
                xpath_b = xpath_data['season_score_b']
                xpath = xpath_f+ str(i) + xpath_b
                
                season_score = driver.find_element(by = By.XPATH, value = xpath)
                bar = season_score.get_attribute("style")

                ratio.append(ratio)

            except NoSuchElementException:
                continue

        return season, ratio
    except TimeoutException:
        return None, None

def note_element(driver, xpath_data):

    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['notes_grid'])))
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_data['notes_grid'])))

        try: ## top
            top_notes = driver.find_element(by = By.XPATH, value = xpath_data['top_notes_num'])
            t_num = len(top_notes.find_elements(by = By.TAG_NAME, value = 'div'))
            top_note = notes_finder(driver, xpath_data, num, 'top')
            

        except NoSuchElementException:
            continue

        try: ## middle
            middle_notes = driver.find_element(by = By.XPATH, value = xpath_data['middle_notes_num'])
            m_num = len(top_notes.find_elements(by = By.TAG_NAME, value = 'div'))
            mid_note = notes_finder(driver, xpath_data, num, 'middle')

        except NoSuchElementException:
            continue

        try: ## base
            base_notes = driver.find_element(by = By.XPATH, value = xpath_data['base_notes_num'])
            b_num = len(top_notes.find_elements(by = By.TAG_NAME, value = 'div'))
            base_note = notes_finder(driver, xpath_data, num, 'base')
        except NoSuchElementException:
            continue
            
        return top_note, mid_note, base_note

    except TimeoutException:
        return None, None, None

def notes_finder(driver, xpath_data, num, type):
    notes = []

    for i in range(1, num+1): ##top note
        xpath_f = xpath_data[type+'_note_f']
        xpath_b = xpath_data[type+'_note_b']
        xpath = xpath_f+ str(i) + xpath_b
        try:
            note = driver.find_element(by = By.XPATH, value = xpath)
            note = note.get_attribute("textContent")
            notes.append(note)
        except NoSuchElementException:
            continue

    return notes

def rating_element(driver, xpath_data):

    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['rating_score'])))
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_data['rating_num'])))

        try:
    
            rating_score = driver.find_element(by = By.XPATH, value = xpath_data['rating_score'])
            rating_num = driver.find_element(by = By.XPATH, value = xpath_data['rating_num'])
            
            rating_score = rating_score.get_attribute("textContent")
            rating_num = rating_num.get_attribute("textContent")

        except NoSuchElementException:
            continue

        return rating_score, rating_num
    except TimeoutException:
        return None, None

def information_crawler(data, xpath_data,chrome_path,chrome_options):
    data = range(2)
    for fragrance in tqdm(data):

        #brand = fragrance['Brand']
        #fr_name = fragrance['Fragrance']
        #url = fragrance['Url']
        url = 'https://www.fragrantica.com/perfume/Hermes/Terre-d-Hermes-17.html'

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.set_window_size(1920, 1080)
            driver.get(url)
        
            accord_text, accord_ratio = accord_element(driver, xpath_data)
            return 

            
        


        except IndexError:
            failed_country_list.append(country_url)

        driver.quit()
    return data, failed_country_list, failed_fragrance_list

def property_element(driver, xpath_data):


    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,xpath_data['property_grid'])))
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, xpath_data['property_grid'])))

        for i in [4,5,7,8]:
            try:
                xpath_f = xpath_data['season_score_f']
                xpath_b = xpath_data['season_score_b']
                xpath = xpath_f+ str(i) + xpath_b
                
                season_score = driver.find_element(by = By.XPATH, value = xpath)
                bar = season_score.get_attribute("style")

                ratio.append(ratio)

            except NoSuchElementException:
                continue

        return season, ratio
    except TimeoutException:
        return None, None

def property_finder(driver, xpath_data, type):
    
if __name__ =="__main__":

    vdisplay = Xvfb(width=1920, height=1080)
    vdisplay.start()
    
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("--remote-debugging-port=9222")
    mobile_emulation = { "deviceName" : "iPhone X" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument('--disable-dev-shm-usage') 
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument("--disable-extensions")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    #user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_LOG'] = "false"
    chrome_path = "/home/dhkim/chromedriver"

    with open('/home/dhkim/Fragrance/xpath.json', 'r') as f:

        
        xpath_data = json.load(f)
        #data = pd.read_csv('/home/dhkim/Fragrance/data/data.csv')
        data = None
        information_crawler(data, xpath_data,chrome_path,chrome_options)

        